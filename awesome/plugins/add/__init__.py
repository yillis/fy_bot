from nonebot import on_command
from nonebot import CommandSession
from nonebot import on_natural_language
from nonebot import NLPSession
from nonebot import IntentCommand

from awesome.util import const
from awesome.util import sqlite


@on_command('add', aliases=['add', ])
async def add(session: CommandSession):
    problem_name = session.get('problem_name', prompt='没有找到你所描述的问题')
    method = session.get('method', prompt='没有找到你所描述的问题')
    await sqlite.update_method(problem_name, method)
    await session.send('添加成功')


@add.args_parser
async def _(session: CommandSession):
    for keywords in const.ADD_KEYWORDS:
        index = session.current_arg_text.find(keywords)
        if index != -1:
            session.state['problem_name'] = session.current_arg_text[0:index]
            session.state['method'] = session.current_arg_text[index:]


@on_natural_language(keywords=[const.ADD_KEYWORDS])
async def _(session: NLPSession):
    return IntentCommand(90.0, 'add', current_arg=session.msg_text)
