from awesome.util.fybot_sqlite import SQLClient, _DB_NAME


async def add_keyword(problem: str, keyword: str):
    keywords = await get_keywords(problem)
    print(keywords)
    if keyword not in keywords:
        keywords.append(keyword)
    sqlite = SQLClient(_DB_NAME)
    await sqlite.data_update(problem, keywords)


async def get_keywords(problem: str) -> list:
    sqlite = SQLClient(_DB_NAME)
    return await sqlite.get_data(problem)