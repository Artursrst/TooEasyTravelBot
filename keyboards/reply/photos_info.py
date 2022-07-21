import requests
import json
import re

def photos_receiving(text:str, quantity:int = 8):
    pattern1 = r'(?<="caption": ")[^"]+'
    find1 = re.findall(pattern1, text)

    pattern2 = r'(?<="destinationId": ")[^"]+'
    find2 = re.findall(pattern2, text)

    if quantity > 10:
        quantity = 10
    elif quantity < 1:
        quantity = 1

    find1 = find1[0:quantity]
    i_number = 0
    for i in find1:
        if 'span' in i:
            pattern = r'(<span.+span>)'
            find = re.split(pattern, i)
            find1[i_number] = find[0] + find[2]
        i_number += 1
    find2 = find2[0:quantity]
    find = find1 + find2
    result = []

    for i in range(len(find1)):
        result.append([find[i], find[i + len(find1)]])

    return result