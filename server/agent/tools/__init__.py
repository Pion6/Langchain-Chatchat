## 导入所有的工具类
from .search_knowledgebase_simple import search_knowledgebase_simple
from .search_knowledgebase_once import search_knowledgebase_once, KnowledgeSearchInput
from .search_knowledgebase_complex import search_knowledgebase_complex, KnowledgeSearchInput
from .calculate import calculate, CalculatorInput
from .weather_check import weathercheck, WhetherSchema
from .shell import shell, ShellInput
from .search_internet import search_internet, SearchInternetInput
from .wolfram import wolfram, WolframInput
from .search_youtube import search_youtube, YoutubeInput
from .arxiv import arxiv, ArxivInput
from .course_schedule import course_schedule_check, CourseScheduleSchema
from .course_schedule2 import course_schedule_check2, CourseScheduleSchema2
from .course_schedule2 import CourseSchedule
