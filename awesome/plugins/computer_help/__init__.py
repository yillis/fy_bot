# standard module

# extend module
from nonebot import on_command
from nonebot import CommandSession
from nonebot import NLPSession
from nonebot import on_natural_language
from nonebot import IntentCommand

# project module
from awesome.util.sql_client import SQLClient
from awesome.plugins.computer_help import problems


@on_command('computer_help', aliases=('电脑坏了', '电脑出问题了', '怎么回事'))
async def computer_help(session: CommandSession):
    problem = session.get('computer_help', prompt='请再详细描述一下你的电脑问题，如果还是不行请找管理员哦。')
    sql_client = SQLClient()
    await session.send(await sql_client.query(problem))


@computer_help.args_parser
async def _(session: CommandSession):
    problem = await problems.evaluate(session.current_arg_text)
    if problem:
        session.state['computer_help'] = problem


@on_natural_language(keywords={'电脑坏', '哈哈哈'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'computer_help', current_arg=session.msg_text)
