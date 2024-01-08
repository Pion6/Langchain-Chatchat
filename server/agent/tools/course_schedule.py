from pydantic import BaseModel, Field
from server.agent import model_container
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate
import requests
Parse_Prompt = """
用户会提出一个关于课程表的问题，你的目标是拆分出用户问题中的用户名和时间 并按照我提供的工具回答。
例如 用户提出的问题是: 王小明老师今天要上哪些课程？
则 提取的市和区是: 王小明 今天
如果用户提出的问题是: 王小明老师要上哪些课程？
则 提取的市和区是: 王小明 None
请注意以下内容:
1. 如果你没有找到时间或用户的内容,则一定要使用 None 替代，否则程序无法运行
2. 如果有其他情况则直接返回缺少信息

现在，这是我的问题：

问题: {question}
"""

Answer_Prompt = """ 
# 角色
你是一名时间管理大师，擅长帮助他人合理规划和利用时间，以提高工作和生活效率。
### 技能1：理解课程表
- 确定用户提供的课程表的有效日期。
- 确定每个课程的起止时间，并注意是否存在重叠。
- 识别课程的重复模式（例如，每周、每两周、每月等）。

下面的内容是我的课程表:{course_schedule}
"""
def course_schedule_check(name: str):
    print("------------course_schedule_check----------------")
    print(name)
    print("------------course_schedule_check----------------")
    url = f"http://10.12.54.64:5000/school/sheet/{name}/今天"
    response = requests.get(url)
    # data = response.json()
    # print("------------returnData----------------")
    # print(data)
    # print("------------returnData----------------")
    model = model_container.MODEL
    # parse_chain = LLMChain(prompt=Parse_Prompt, llm=model, memory=None)
    # parse_ans = parse_chain.run(query)
    # print("------------parse_ans----------------")
    # # print(parse_ans)
    # print("------------parse_ans----------------")
    answer_template = ChatPromptTemplate.from_template(Answer_Prompt)
    ans_chain = LLMChain(prompt=answer_template, llm=model, memory=None)
    ans = ans_chain.run(course_schedule=response.text)
    print("------------finally_ans----------------")
    print(ans)
    print("------------finally_ans----------------")
    return ans


class CourseScheduleSchema(BaseModel):
    name: str = Field(description="应该是用户的姓名,例如: '''王小明老师明天的课程表是什么样的'''答案为: 王小明。如果没有人名可以返回None")
