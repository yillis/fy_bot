from awesome.util.fybot_sqlite import SQLClient, _DB_NAME


async def get_ask_problem(text: str) -> str:
    """"""
    data = await get_ask_data()
    dic = {}
    for problem in data:
        for keyword in data[problem]:
            if text.find(keyword) != -1:
                weight = 1
                dic[problem] = dic.get(problem, 0) + weight
    return '' if len(dic) == 0 else max(dic, key=dic.get)


async def get_method(problem: str) -> str:
    sqlite = SQLClient()
    return await sqlite.method_query(problem)


async def get_ask_data():
    sqlite = SQLClient(_DB_NAME)
    return await sqlite.name_and_data_query()


async def get_ask_keyword():
    sqlite = SQLClient(_DB_NAME)
    return await sqlite.show_problems()