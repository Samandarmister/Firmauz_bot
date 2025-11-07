def convert_to_cyrillic(text):
    text = text.replace("'", 'ʻ').replace('‘', 'ʻ').replace('’', 'ʻ')

    translit_map = {
        # 'shch': 'щ',  # Olib tashlandi, chunki bu O‘zbek tilida kerak emas
        'ch': 'ч', 'sh': 'ш', 'yo': 'ё', 'yu': 'ю', 'ya': 'я',
        'oʻ': 'ў', 'gʻ': 'ғ', 'ʻ': 'ъ', 'a': 'а', 'b': 'б', 'v': 'в',
        'g': 'г', 'd': 'д', 'e': 'е', 'z': 'з', 'i': 'и', 'y': 'й',
        'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
        'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'x': 'ҳ',
        'ts': 'ц', 'q': 'қ', 'h': 'ҳ', 'j': 'ж'
    }

    sorted_keys = sorted(translit_map.keys(), key=lambda x: (-len(x), x))
    result = []
    i = 0

    while i < len(text):
        matched = False
        for key in sorted_keys:
            end = i + len(key)
            if end > len(text):
                continue
            substring = text[i:end].lower()
            if substring == key.lower():
                base = translit_map[key]
                original = text[i:end]
                if original.isupper():
                    converted = base.upper()
                elif original.istitle():
                    converted = base.capitalize()
                else:
                    converted = base.lower()
                result.append(converted)
                i = end
                matched = True
                break
        if not matched:
            result.append(text[i])
            i += 1

    return ''.join(result)


def convert_to_latin(text):
    translit_map = {
        'Щ': 'Shch', 'щ': 'shch',
        'Шаҳ': 'Shah', 'шаҳ': 'shah',  # Maxsus qayta ishlash
        'Ш': 'Sh', 'ш': 'sh',
        'Ч': 'Ch', 'ч': 'ch',
        'Ў': 'Oʻ', 'ў': 'oʻ',
        'Ғ': 'Gʻ', 'ғ': 'gʻ',
        'Ҳ': 'X', 'ҳ': 'x',
        'Қ': 'Q', 'қ': 'q',
        'Ё': 'Yo', 'ё': 'yo',
        'Ю': 'Yu', 'ю': 'yu',
        'Я': 'Ya', 'я': 'ya',
        'ъ': "'", 'ь': '',
        'А': 'A', 'а': 'a',
        'Б': 'B', 'б': 'b',
        'В': 'V', 'в': 'v',
        'Г': 'G', 'г': 'g',
        'Д': 'D', 'д': 'd',
        'Е': 'E', 'е': 'e',
        'Ж': 'J', 'ж': 'j',
        'З': 'Z', 'з': 'z',
        'И': 'I', 'и': 'i',
        'Й': 'Y', 'й': 'y',
        'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l',
        'М': 'M', 'м': 'm',
        'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o',
        'П': 'P', 'п': 'p',
        'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's',
        'Т': 'T', 'т': 't',
        'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f',
        'Х': 'X', 'х': 'x',
        'Ц': 'Ts', 'ц': 'ts',
        'Ы': 'Y', 'ы': 'y',
        'Э': 'E', 'э': 'e',
    }

    sorted_keys = sorted(translit_map.keys(), key=lambda x: (-len(x), x))
    result = []
    i = 0
    
    while i < len(text):
        matched = False
        for key in sorted_keys:
            end = i + len(key)
            if end > len(text):
                continue
            substring = text[i:end]
            if substring == key:
                base = translit_map[key]
                result.append(base)
                i = end
                matched = True
                break
        if not matched:
            result.append(text[i])
            i += 1
            
    return ''.join(result)

