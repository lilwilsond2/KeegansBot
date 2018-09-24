import requests
import yaml

from helper import getJsonObjectsFromUrl, beautifyList, embedImage


def monsterShorthandReplace(monsterName):
    shorthandDict = yaml.load(open("settings/monsterShorthand.yml"))
    for monster in shorthandDict:
        if monsterName.lower() in [shorthand.lower() for shorthand in shorthandDict[monster]]:
            monsterName = monster
            break
    return monsterName.lower()


def getMonsterData(monsterName):
    monsterDataUrl = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/" \
                     "source_data/monsters/monster_weaknesses.json"
    monsters: dict = getJsonObjectsFromUrl(monsterDataUrl)
    monsters = {name.lower(): resistances for name, resistances in monsters.items()}
    return monsters[monsterName]


def getMonsterId(monsterName):
    monsterDataUrl = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/" \
                     "source_data/monsters/monster_base.csv"
    monsterData = requests.get(monsterDataUrl).text
    lines = monsterData.splitlines()
    for line in lines:
        tokens = line.split(",")
        if tokens[1].lower() == monsterName:
            return tokens[0]


def getMonsterImageUrl(monsterName):
    return "https://github.com/gatheringhallstudios/MHWorldData/tree/master/" \
           "images/monster/{}.png".format(getMonsterId(monsterName))


def manageMudResistances(monsterInfo, normalResistances):
    if 'alt' not in monsterInfo:
        return normalResistances
    mudResistances = monsterInfo['alt']
    for updatedResistance in mudResistances:
        normalResistances[updatedResistance] = normalResistances[updatedResistance] + \
                                               "({})".format(starsForValue(mudResistances[updatedResistance]))
    return normalResistances


def getFormattedMonsterOutput(monsterName):
    officialName = monsterShorthandReplace(monsterName)
    monsterInfo = getMonsterData(officialName)
    return "{}\n{}".format(
        embedImage(getMonsterImageUrl(officialName), monsterName, ""),
        beautifyList(getResistances(monsterInfo)))


def getResistances(monsterInfo) -> list:
    resistances = getNormalResistances(monsterInfo)
    resistances = manageMudResistances(monsterInfo, resistances)
    return ["{} {}".format(x, resistances[x]) for x in resistances]


def getNormalResistances(monsterInfo):
    resistances = monsterInfo['normal']
    output = {}
    for resistance in resistances:
        output[resistance] = starsForValue(resistances[resistance])
    return output


def starsForValue(value):
    stars = ""
    for x in range(value):
        stars += "\*"
    stars = handleImmune(stars)
    return stars


def handleImmune(stars):
    return "X" if stars == "" else stars


print(getFormattedMonsterOutput("barry"))