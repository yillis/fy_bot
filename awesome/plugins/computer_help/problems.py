_PROBLEMS = {
    '电脑蓝屏': {
        ('电脑蓝屏', 100.0),
        ('蓝屏', 0.6),
        ('蓝', 0.2)
    },
    '无法上网': {
        ('网络', 0.3),
        ('无法上网', 100),
        ('连不上WIFI', 0.5)
    }
}


async def evaluate(text: str) -> str:
    dic = dict()
    for problem in _PROBLEMS:
        for key_word, weight in _PROBLEMS[problem]:
            if text.find(key_word):
                if key_word in dic:
                    dic[key_word] += weight
                else:
                    dic[key_word] = weight
    return max(dic, key=dic.get)
