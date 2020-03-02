from nonebot import on_command
from nonebot import CommandSession
from nonebot import on_natural_language
from nonebot import NLPSession
from nonebot import IntentCommand

import awesome.plugins.update.data_source


@on_command('update', aliases=['update', ])
async def update(session: CommandSession):
    problem_name = session.get('problem_name', prompt='没有找到你所描述的问题')
    method = session.get('method', prompt='没有找到你所描述的问题')
    await awesome.plugins.update.data_source.update_method(problem_name, method)
    await session.send('添加成功')


@update.args_parser
async def _(session: CommandSession):
    awaited_keyword = ['的解决方法是', '的方法是']
    for keywords in awaited_keyword:
        index = session.current_arg_text.find(keywords)
        if index != -1:
            session.state['problem_name'] = session.current_arg_text[0:index]
            session.state['method'] = session.current_arg_text[index + len(keywords):]


# @on_natural_language(keywords=['的解决方法是', '的方法是'])
# async def _(session: NLPSession):
#     probability = 0.0
#     awaited_keyword = await const.UPDATE_KEYWORD
#     one = 100.0 / len(awaited_keyword)
#     for keywords in awaited_keyword:
#         if session.msg_text.find(keywords) != -1:
#             probability += one
#     return IntentCommand(probability, 'update', current_arg=session.msg_text)
