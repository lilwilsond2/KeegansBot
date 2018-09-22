import yaml

from helper import getJsonObjectsFromUrl, beautifyList


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
    return monsters[monsterShorthandReplace(monsterName)]


def manageMudResistances(monsterInfo, normalResistances):
    if 'alt' not in monsterInfo:
        return normalResistances
    mudResistances = monsterInfo['alt']
    for updatedResistance in mudResistances:
        normalResistances[updatedResistance] = normalResistances[updatedResistance] + \
                                               "({})".format(starsForValue(mudResistances[updatedResistance]))
    return normalResistances


def getFormattedMonsterOutput(monsterName):
    monsterInfo = getMonsterData(monsterName)
    return beautifyList(getResistances(monsterInfo))


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
