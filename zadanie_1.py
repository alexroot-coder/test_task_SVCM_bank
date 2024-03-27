import json


def find_by_key(this_data, target):
    """
    Неизвестно, какой уровень вложенности, поэтому проверка каждого value пока не будет найден нужный target_value
    :param this_data: исходный nested dict
    :param target: искомый item
    :return:  значение (ключ 'value')
    """
    for key, value in this_data.items():
        if isinstance(value, dict):  # проверяем какой сейчас элемент при каждом углублении в текущем item'e
            yield from find_by_key(value, target)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from find_by_key(item, target)
        elif value == target:  # как только найден нужный target_value возвращаем его value
            yield this_data.get('value')


with open("json_data/data.json", 'r', encoding="utf-8") as f:
    data = json.load(f)


print(*[_ for _ in find_by_key(data, 1024)])

