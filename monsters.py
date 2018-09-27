import requests
import yaml

from helper import getJsonObjectsFromUrl, beautifyList

WEAKNESSES_JSON = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/" \
                  "source_data/monsters/monster_weaknesses.json"

MONSTER_BASE_CSV = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/" \
                   "source_data/monsters/monster_base.csv"

TRIBAL_IMAGE = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/images/monster/{}.png"


def getFormattedMonsterOutput(monsterName):
    officialName = getOfficialMonsterName(monsterName)
    monsterInfo = getMonsterData(officialName)
    return "{}\n{}".format(
            getMonsterImageUrl(officialName),
            beautifyList(getResistances(monsterInfo)))


def getOfficialMonsterName(monsterName):
    shorthandDict = yaml.load(open("settings/monsterShorthand.yml"))
    for monster in shorthandDict:
        if monsterName.lower() in [shorthand.lower() for shorthand in shorthandDict[monster]]:
            monsterName = monster
            break
    return monsterName.lower()


def getMonsterData(monsterName):
    monsters: dict = getJsonObjectsFromUrl(WEAKNESSES_JSON)
    monsters = {name.lower(): resistances for name, resistances in monsters.items()}
    return monsters[monsterName]


def getMonsterId(monsterName):
    monsterData = requests.get(MONSTER_BASE_CSV).text
    lines = monsterData.splitlines()
    for line in lines:
        tokens = line.split(",")
        if tokens[1].lower() == monsterName:
            return tokens[0]


def getMonsterImageUrl(monsterName):
    return TRIBAL_IMAGE.format(getMonsterId(monsterName))


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


def manageMudResistances(monsterInfo, resistances):
    if 'alt' not in monsterInfo:
        return resistances
    mudResistances = monsterInfo['alt']
    for updatedResistance in mudResistances:
        resistances[updatedResistance] = resistances[updatedResistance] + \
                                         "({})".format(starsForValue(mudResistances[updatedResistance]))
    return resistances


def starsForValue(value):
    stars = ""
    for x in range(value):
        stars += "\*"
    stars = handleImmune(stars)
    return stars


def handleImmune(stars):
    return "X" if stars == "" else stars
