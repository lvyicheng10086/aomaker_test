from aomaker.maker.models import Operation

def custom_naming(path:str,method:str,operation:Operation) -> str:
    parts = path.split('/')
    parts = [p for p in parts if p]
    print(parts)
    last_two = parts[-2:]

    if len(last_two) > 1:
        # capitalize
        # 输出：返回一个新的字符串，新字符串的首字母大写，其余字母小写。
        # 注意事项：如果字符串为空或首字符不是字母，则不会进行任何修改
        first_part = last_two[0].capitalize()

        last_part = last_two[1]
        if last_part and last_part[0].islower():
            last_part = last_part[0].upper() + last_part[1:]
        camel_case = first_part + last_part
    elif len(last_two) == 1:
        last_part = last_two[0]
        if last_part and last_part[0].islower():
            camel_case = last_part[0].upper() + last_part[1:]
        else:
            camel_case = last_part.capitalize()
    else:
        camel_case = ''

    return f"{camel_case}API"


if __name__ == '__main__':
    print(custom_naming("/sso/platform/login/info/get-by-token", "POST", Operation()))