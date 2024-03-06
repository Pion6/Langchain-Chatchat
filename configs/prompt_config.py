unified_answer = "抱歉，这个问题你可能需要询问老师哦"

PROMPT_TEMPLATES = {
    "llm_chat": {
        "default":
            '<指令>请解读用户的问题并根据他们的问题提供详细的回答。</指令>'
            '以下是用户问题：{{ input }}',

        "with_history":
            'The following is a friendly conversation between a human and an AI. '
            'The AI is talkative and provides lots of specific details from its context. '
            'Current conversation:\n'
            '{history}\n'
            'Human: {input}\n'
            'AI:',

        "py":
            '你是一个聪明的代码助手，请你给我写出简单的py代码。 \n'
            '{{ input }}',
        "empty":
            '{{ input }}',
    },


    "knowledge_base_chat": {
    # 请尽量根据已知信息回答问题
    # 如果有已知信息，请尽量根据已知信息的答案回答问题,尽量不要自己发挥
        "default":
            '<指令>如果有和问题匹配的已知信息，请尽量根据已知信息的回答进行回答,并且请尽量完整使用匹配的回答不要遗漏。如果问题和已知信息中的问题不匹配，请尽可能详尽的回答用户问题</指令>\n'
            '<已知信息>{{ context }}</已知信息>\n'
            '<问题>{{ question }}</问题>\n',

        "text":
            '<指令>如果有和问题匹配的已知信息，请尽量根据已知信息的回答进行回答,并且请尽量完整使用匹配的回答不要遗漏。如果问题和已知信息中的问题不匹配，请尽可能详尽的回答用户问题</指令>\n'
            '<已知信息>{{ context }}</已知信息>\n'
            '<问题>{{ question }}</问题>\n',

        "empty":  # 搜不到知识库的时候使用
            '请你回答我的问题:\n'
            '{{ question }}\n\n',

        # "default":
        #     '<指令>根据已知信息，简洁和专业的来回答问题，答案请使用中文。 </指令>\n'
        #     '<已知信息>{{ context }}</已知信息>\n'
        #     '<问题>{{ question }}</问题>\n',
    },


    "search_engine_chat": {
        "default":
            '<指令>这是我搜索到的互联网信息，请你根据这些信息进行提取并有调理，简洁的回答问题。'
            '<已知信息>{{ context }}</已知信息>\n'
            '<问题>{{ question }}</问题>\n',

        "search":
            '<指令>根据已知信息，简洁和专业的来回答问题。 </指令>\n'
            '<已知信息>{{ context }}</已知信息>\n'
            '<问题>{{ question }}</问题>\n',
    },


    "agent_chat": {
        "default":
            'Answer the following questions as best you can. If it is in order, you can use some tools appropriately. '
            'You have access to the following tools:\n\n'
            '{tools}\n\n'
            'Use the following format:\n'
            'Question: the input question you must answer1\n'
            'Thought: you should always think about what to do and what tools to use.\n'
            'Action: the action to take, should be one of [{tool_names}]\n'
            'Action Input: the input to the action\n'
            'Observation: the result of the action\n'
            '... (this Thought/Action/Action Input/Observation can be repeated zero or more times)\n'
            'Thought: I now know the final answer\n'
            'Final Answer: the final answer to the original input question\n'
            'Begin!\n\n'
            'history: {history}\n\n'
            'Question: {input}\n\n'
            'Thought: {agent_scratchpad}\n',

        "ChatGLM3":
            'You can answer using the tools, or answer directly using your knowledge without using the tools. '
            'Respond to the human as helpfully and accurately as possible.\n'
            'You have access to the following tools:\n'
            '{tools}\n'
            'Use a json blob to specify a tool by providing an action key (tool name) '
            'and an action_input key (tool input).\n'
            'Valid "action" values: "Final Answer" or  [{tool_names}]'
            'Provide only ONE action per $JSON_BLOB, as shown:\n\n'
            '```\n'
            '{{{{\n'
            '  "action": $TOOL_NAME,\n'
            '  "action_input": $INPUT\n'
            '}}}}\n'
            '```\n\n'
            'Follow this format:\n\n'
            'Question: input question to answer\n'
            'Thought: consider previous and subsequent steps\n'
            'Action:\n'
            '```\n'
            '$JSON_BLOB\n'
            '```\n'
            'Observation: action result\n'
            '... (repeat Thought/Action/Observation N times)\n'
            'Thought: I know what to respond\n'
            'Action:\n'
            '```\n'
            '{{{{\n'
            '  "action": "Final Answer",\n'
            '  "action_input": "Final response to human"\n'
            '}}}}\n'
            'Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. '
            'Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.\n'
            'history: {history}\n\n'
            'Question: {input}\n\n'
            'Thought: {agent_scratchpad}',
    }
}
