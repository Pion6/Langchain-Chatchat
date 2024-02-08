from pydantic import BaseModel, Field
from server.agent import model_container
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate
from langchain.tools import BaseTool
from typing import Union, Optional
import requests




def course_schedule_check2(parm: str):
    parm_obj = eval(parm)
    # print(parm_obj)
    if len(parm_obj) > 1:
        url = f"http://127.0.0.1:5000/school/sheet/{parm_obj[0]}/{parm_obj[1]}"
    else:
        url = f"http://127.0.0.1:5000/school/sheet/{parm_obj[0]}/今天"

    response = requests.get(url)
    return response.text


class CourseScheduleSchema2(BaseModel):
    name: str = Field(
        description="应该是用户的姓名,例如: '''王小明老师明天的课程表是什么样的'''答案为: 王小明。如果没有人名可以返回None")
    time: Optional[str] = Field(description="应该是用户的时间,例如: '''王小明老师明天的课程表是什么样的'''答案为: 今天。如果没有人名或时间可以返回None")
