import re

def get_mainlabel(text:str):
    pattern1 = r'(?<="label": ")[^"]+'
    find1 = re.findall(pattern1, text)

    mainlabel = find1[0]

    return mainlabel