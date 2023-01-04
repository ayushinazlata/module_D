from django import template


register = template.Library()


@register.filter()
def censor(value):
    bad_word = ['погиб', 'мэр', 'спецоперация', 'жертва']
    for word in value.split():
        for i in bad_word:
            if i.lower() in word.lower().replace(',.:;/-\\""', ''):
                value = value.replace(i, f"{i[0]}{'*' * (len(i) - 1)}")

    if not isinstance(value, str):
        raise TypeError(f'Фильтр применяется к неразрешенному типу {type(value)}\n'
                        f'Разрешенный тип str')

    return value
