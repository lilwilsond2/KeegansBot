import json
import sqlite3

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


def downloadLatestData(fileName="mhw.db"):
    url = requests.get("https://github.com/gatheringhallstudios/MHWorldData/releases/latest/").url
    url = url.replace("tag", "download") + "/{}".format(fileName)
    f = open(fileName, "wb")
    f.write(requests.get(url).content)
    f.close()


def getDatabaseConnection(fileName="mhw.db"):
    return sqlite3.connect(fileName)
