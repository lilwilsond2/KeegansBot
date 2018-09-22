from helper import getJsonObjectsFromUrl, beautifyList


def monsterLookup(monsterName):
    monsterDataUrl = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/" \
                     "source_data/monsters/monster_weaknesses.json"
    monsters = getJsonObjectsFromUrl(monsterDataUrl)
    return monsters[monsterName]


def manageMudResistances(monsterInfo, normalResistances):
    if 'alt' not in monsterInfo:
        return normalResistances
    mudResistances = monsterInfo['alt']
    for updatedResistance in mudResistances:
        normalResistances[updatedResistance] = normalResistances[updatedResistance] + \
                                               "({})".format(starsForValues(mudResistances[updatedResistance]))
    return normalResistances


def getFormattedMonsterOutput(monsterName):
    monsterInfo = monsterLookup(monsterName)
    return beautifyList(getResistances(monsterInfo))


def getResistances(monsterInfo) -> list:
    resistances = getNormalResistances(monsterInfo)
    resistances = manageMudResistances(monsterInfo, resistances)
    return ["{} {}".format(x, resistances[x]) for x in resistances]


def getNormalResistances(monsterInfo):
    resistances = monsterInfo['normal']
    output = {}
    for resistance in resistances:
        output[resistance] = starsForValues(resistances[resistance])
    return output


def starsForValues(value):
    stars = ""
    for x in range(value):
        stars += "\*"
    stars = handleImmune(stars)
    return stars


def handleImmune(stars):
    stars = "X" if stars == "" else stars
    return stars
