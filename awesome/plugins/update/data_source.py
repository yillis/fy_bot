from awesome.util.repair_sqlite import SQLClient


async def get_problem_and_method(text: str) -> (str, str):
    keywords = await get_update_keyword()
    for keyword in keywords:
        index = text.find(keyword)
        if index != -1:
            return text[0:index], text[index + len(keyword):]
    return '', ''


async def update_method(problem: str, method: str):
    sqlite = SQLClient(_DB_NAME)
    await sqlite.method_update(problem, method)


async def get_update_keyword() -> list:
    return ['的解决方法是', '的方法是']
