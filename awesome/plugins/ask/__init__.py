from nonebot import on_command
from nonebot import CommandSession
from nonebot import on_natural_language
from nonebot import NLPSession
from nonebot import IntentCommand

from awesome.util import const


@on_command('ask', aliases=['ask', ])
async def ask(session: CommandSession):
    # do some thing
    return


@ask.args_parser
async def _(session: CommandSession):
    # to get the problem
    return


@on_natural_language(keywords=[const.ASK_KEYWORDS])
async def _(session: NLPSession):
    return IntentCommand(90.0, 'ask', current_arg=)
