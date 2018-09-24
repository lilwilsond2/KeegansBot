import json

import requests


def getJsonObjectsFromUrl(requestUrl) -> list:
    apiData = requests.get(requestUrl).text
    apiObjects = json.loads(apiData)
    return apiObjects


def beautifyList(list):
    output = list.pop(0)
    for armorPiece in list:
        output += "\n{}".format(armorPiece)
    return output


def embedImage(imageUrl, hoverText, altText):
    return "![{}]({} {})".format(altText, imageUrl, hoverText)
