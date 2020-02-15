from nonebot import on_command
from nonebot import CommandSession
from nonebot import on_natural_language
from nonebot import NLPSession
from nonebot import IntentCommand

from awesome.util import const
from awesome.util import sqlite


@on_command('ask', aliases=['ask', ])
async def ask(session: CommandSession):
    problem_name = session.get('problem_name', prompt='请再详细描述一下你的电脑问题，如果还是不行请找管理员哦。')
    method = await sqlite.get_method(problem_name)
    await session.send(method)


@ask.args_parser
async def _(session: CommandSession):
    problem_name = await sqlite.get_problem_name(session.current_arg_text)
    if problem_name:
        session.state['problem_name'] = problem_name


@on_natural_language(keywords=[const.ASK_KEYWORDS])
async def _(session: NLPSession):
    probability = 0.0
    one = 100.0 / len(const.ASK_KEYWORDS)
    for keywords in const.ASK_KEYWORDS:
        if session.msg_text.find(keywords) != -1:
            probability += one
    return IntentCommand(probability, 'ask', current_arg=session.msg_text)
