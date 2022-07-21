import requests
import json
import re

def info_for_high_and_low_price(text:str, q, h):
    pattern1 = r'(?<="label": ")[^"]+'
    find1 = re.findall(pattern1, text)

    pattern2 = r'(?<="distance": ")[^( miles")]+'
    find2 = re.findall(pattern2, text)

    pattern3 = r'(?<="current": ")[^"]+'
    find3 = re.findall(pattern3, text)

    pattern4 = r'(?<="streetAddress": ")[^"]+'
    find4 = re.findall(pattern4, text)

    pattern5 = r'(?<="name": ")[^"]+'
    find5 = re.findall(pattern5, text)

    mainlabel = find1[0]
    newfind1 = []
    newfind2 = []
    newfind3 = []
    newfind4 = []
    index = 0
    for i in find1:
        if i == mainlabel:
            newfind1.append(find2[index])
            newfind2.append(find3[index])
            newfind3.append(find4[index])
            newfind4.append(find5[index])
        index += 1
        if index > 20:
            break
    doplist = []
    for i in newfind2:
        doplist.append(int(i[1:]))

    rnewfind1 = []
    rnewfind2 = []
    rnewfind3 = []
    rnewfind4 = []
    if h =='h':
        forsortlist = sorted(set(sorted(doplist, reverse=True)), reverse=True)
    else:
        forsortlist = sorted(set(sorted(doplist)))
    for i in forsortlist:
        index = 0
        for j in newfind2:
            if i == int(j[1:]):
                rnewfind1.append(newfind1[index])
                rnewfind2.append(newfind2[index])
                rnewfind3.append(newfind3[index])
                rnewfind4.append(newfind4[index])
            index += 1

    rnewfind1 = rnewfind1[:q]
    rnewfind2 = rnewfind2[:q]
    rnewfind3 = rnewfind3[:q]
    rnewfind4 = rnewfind4[:q]

    return mainlabel, rnewfind1, rnewfind2, rnewfind3, rnewfind4