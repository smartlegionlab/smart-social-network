import unicodedata


def transliterate_cyrillic(text, sep='-'):
    cyrillic_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    }

    text = unicodedata.normalize('NFKD', text.lower())

    result = []
    for char in text:
        if char in cyrillic_map:
            result.append(cyrillic_map[char])
        elif char == ' ' or char == '-':
            if result and result[-1] != sep:
                result.append(sep)
        elif char.isalnum():
            result.append(char)

    return ''.join(result).strip(sep)
