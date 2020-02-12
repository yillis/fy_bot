# standard module

# extend module
from nonebot import on_command
from nonebot import CommandSession

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
    session.state['computer_help'] = await problems.evaluate(session.current_arg_text)
