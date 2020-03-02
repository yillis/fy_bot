from nonebot import on_command
from nonebot import CommandSession
from nonebot import on_natural_language
from nonebot import NLPSession
from nonebot import IntentCommand

import awesome.plugins.ask.data_source


@on_command('ask', aliases=['ask', ])
async def ask(session: CommandSession):
    problem_name = session.get('problem', prompt='请再详细描述一下你的电脑问题，如果还是不行请找管理员哦')
    method = await awesome.plugins.ask.data_source.get_method(problem_name)
    if not method:
        method = "没有找到解决方法哦，请联系管理员添加解决方法"
    await session.send(method)


@ask.args_parser
async def _(session: CommandSession):
    problem = await awesome.plugins.ask.data_source.get_ask_problem(session.current_arg_text)
    if problem:
        session.state['problem'] = problem


# @on_natural_language(keywords=[const.ASK_KEYWORD])
# async def _(session: NLPSession):
#     probability = 0.0
#     one = 100.0 / len(const.ASK_KEYWORD)
#     for keywords in const.ASK_KEYWORD:
#         if session.msg_text.find(keywords) != -1:
#             probability += one
#     return IntentCommand(probability, 'ask', current_arg=session.msg_text)
