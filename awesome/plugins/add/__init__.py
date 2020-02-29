from nonebot import on_command
from nonebot import CommandSession

import awesome.plugins.add.data_source
from awesome.util import fybot_sqlite


@on_command('add', aliases=['add', ])
async def add(session: CommandSession):
    problem_name = session.get('problem_name', prompt='没有找到你所描述的问题')
    keyword = session.get('keyword', prompt='没有找到你所描述的方法')
    await awesome.plugins.add.data_source.add_keyword(problem_name, keyword)
    await session.send('添加成功')


@add.args_parser
async def _(session: CommandSession):
    split_text = session.current_arg_text.split(' ')
    if len(split_text) >= 2:
        session.state['problem_name'] = split_text[0]
        session.state['keyword'] = split_text[1]

