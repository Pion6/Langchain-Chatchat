from fastapi import Body
from fastapi.responses import StreamingResponse
from configs import LLM_MODELS, TEMPERATURE
from server.utils import wrap_done, get_ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import AsyncIterable
import asyncio
import json
from server.utils import BaseResponse, ListResponse, run_in_thread_pool
from langchain.prompts.chat import ChatPromptTemplate
from typing import List, Optional, Union
from server.chat.utils import History
from langchain.prompts import PromptTemplate
from server.utils import get_prompt_template
from server.memory.conversation_db_buffer_memory import ConversationBufferDBMemory
from server.db.repository import add_message_to_db
from server.callback_handler.conversation_callback_handler import ConversationCallbackHandler
from langchain.chains.router import MultiPromptChain  # 导入多提示链
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate
from configs.answer_config import answer_template


async def chat_router_chain(query: str = Body(..., description="用户输入", examples=["恼羞成怒"]),
                            conversation_id: str = Body("3344", description="对话框ID"),
                            history_len: int = Body(-1, description="从数据库中取历史消息的数量"),
                            history: Union[int, List[History]] = Body([],
                                                                      description="历史对话，设为一个整数可以从数据库中读取历史消息",
                                                                      examples=[[
                                                                          {"role": "user",
                                                                           "content": "我们来玩成语接龙，我先来，生龙活虎"},
                                                                          {"role": "assistant", "content": "虎头虎脑"}]]
                                                                      ),
                            stream: bool = Body(False, description="流式输出"),
                            model_name: str = Body(LLM_MODELS[0], description="LLM 模型名称。"),
                            temperature: float = Body(TEMPERATURE, description="LLM 采样温度", ge=0.0, le=1.0),
                            max_tokens: Optional[int] = Body(None,
                                                             description="限制LLM生成Token数量，默认None代表模型最大值"),
                            # top_p: float = Body(TOP_P, description="LLM 核采样。勿与temperature同时设置", gt=0.0, lt=1.0),
                            prompt_name: str = Body("default",
                                                    description="使用的prompt模板名称(在configs/prompt_config.py中配置)"),
                            ):
    classify_prompt = '''<提示>你具有很强的分类能力，你现在的任务是帮助我对问题进行分类，如果问题符合种类的描述，请输出种类名称，注意仅需要输出问题的种类</提示>
        现在有以下几种问题种类的数据：
        <标签种类>
    {tag}\t<标签：default>:<问题种类：不属于以上任何一个分类，则属于默认问题>
        </标签种类>
    <提示>注意问题名称一定属于上述问题中的一种！！！请精准给出问题种类,并输出以下内容之一：{options}</提示>
    <问题>请给出以下问题的标签：{query}</问题>'''

    classify_prompt_template = ChatPromptTemplate.from_template(classify_prompt)
    model = get_ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        max_tokens=None,
    )
    options = ""
    tag = ""
    for i in answer_template:
        tag += "\t\t<标签：{}>:<问题种类：{}>\n".format(i["name"], i["description"])
        options += "<{}/>或".format(i["name"])
    options += "<default/>"
    chain = LLMChain(prompt=classify_prompt_template, llm=model, memory=None)
    res = chain.run(tag=tag, query=query, options=options)

    async def chat_iterator(res: str) -> AsyncIterable[str]:
        nonlocal history, max_tokens
        callback = AsyncIteratorCallbackHandler()
        callbacks = [callback]
        memory = None
        category = []
        is_default = 0
        category_prompt = ""
        for j in answer_template:
            if j["name"] in res:
                is_default = is_default + 1
                category.append(j["name"])
                category_prompt = "请重复以下这段话:" + j["prompt_template"]

        if len(category) == 0 or len(category) == len(answer_template):
            category_prompt = query
        if conversation_id:
            message_id = add_message_to_db(chat_type="llm_chat", query=category_prompt, conversation_id=conversation_id)
            # 负责保存llm response到message db
            conversation_callback = ConversationCallbackHandler(conversation_id=conversation_id, message_id=message_id,
                                                                chat_type="llm_chat",
                                                                query=category_prompt)
            callbacks.append(conversation_callback)

        if isinstance(max_tokens, int) and max_tokens <= 0:
            max_tokens = None

        model = get_ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            callbacks=callbacks,
        )

        if history:  # 优先使用前端传入的历史消息
            history = [History.from_data(h) for h in history]
            prompt_template = get_prompt_template("llm_chat", prompt_name)
            input_msg = History(role="user", content=prompt_template).to_msg_template(False)
            chat_prompt = ChatPromptTemplate.from_messages(
                [i.to_msg_template() for i in history] + [input_msg])
        elif conversation_id and history_len > 0:  # 前端要求从数据库取历史消息
            # 使用memory 时必须 prompt 必须含有memory.memory_key 对应的变量
            prompt = get_prompt_template("llm_chat", "with_history")
            chat_prompt = PromptTemplate.from_template(prompt)
            # 根据conversation_id 获取message 列表进而拼凑 memory
            memory = ConversationBufferDBMemory(conversation_id=conversation_id,
                                                llm=model,
                                                message_limit=history_len)
        else:
            prompt_template = get_prompt_template("llm_chat", prompt_name)
            input_msg = History(role="user", content=prompt_template).to_msg_template(False)
            chat_prompt = ChatPromptTemplate.from_messages([input_msg])

        chain = LLMChain(prompt=chat_prompt, llm=model, memory=memory)

        # Begin a task that runs in the background.
        task = asyncio.create_task(wrap_done(
            chain.acall({"input": category_prompt}),
            callback.done),
        )

        if stream:
            async for token in callback.aiter():
                # Use server-sent-events to stream the response
                yield json.dumps(
                    {"text": token, "message_id": message_id},
                    ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps(
                {"text": answer, "message_id": message_id},
                ensure_ascii=False)

        await task

    return StreamingResponse(chat_iterator(res), media_type="text/event-stream")
