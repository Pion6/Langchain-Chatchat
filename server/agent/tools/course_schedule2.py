from pydantic import BaseModel, Field
from server.agent import model_container
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate
from langchain.tools import BaseTool
from typing import Union, Optional
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


def course_schedule_check2(parm: str):
    parm_obj = eval(parm)
    if 'time' in parm_obj:
        url = f"http://10.12.54.64:5000/school/sheet/{parm_obj['name']}/{parm_obj['time']}"
    else:
        url = f"http://10.12.54.64:5000/school/sheet/{parm_obj['name']}/今天"

    response = requests.get(url)
    return response.text


class CourseScheduleSchema2(BaseModel):
    name: str = Field(
        description="应该是用户的姓名,例如: '''王小明老师明天的课程表是什么样的'''答案为: 王小明。如果没有人名可以返回None")
    time: Optional[str] = Field(description="应该是用户的时间,例如: '''王小明老师明天的课程表是什么样的'''答案为: 今天。如果没有人名或时间可以返回None")
