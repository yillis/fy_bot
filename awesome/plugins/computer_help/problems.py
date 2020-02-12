_PROBLEMS = {
    '电脑蓝屏': {
        ('电脑蓝屏', 100.0),
        ('蓝屏', 0.6),
        ('蓝', 0.2)
    },
    '无法上网': {
        ('网络', 0.3),
        ('无法上网', 100),
        ('连不上WIFI', 0.5),
        ('上不了网', 100)
    }
}


async def evaluate(text: str) -> str:
    dic = dict()
    for problem in _PROBLEMS:
        for key_word, weight in _PROBLEMS[problem]:
            if text.find(key_word) != -1:
                if problem in dic:
                    dic[problem] += weight
                else:
                    dic[problem] = weight
    return None if len(dic) == 0 else max(dic, key=dic.get)
