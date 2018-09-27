import yaml

from helper import beautifyList, getDatabaseConnection

ID = "select id from monster_text where name = ? COLLATE NOCASE"

FROM_MONSTER_BY_NAME = "from monster " \
                       "join monster_text m on monster.id = m.id " \
                       "where m.name = :monsterName " \
                       "COLLATE NOCASE"

NORMAL_RESIST_SQL = "select " \
                    "weakness_fire as fire, " \
                    "weakness_water as water, " \
                    "weakness_thunder as thunder, " \
                    "weakness_ice as ice, " \
                    "weakness_dragon as dragon, " \
                    "weakness_poison as poison, " \
                    "weakness_sleep as sleep, " \
                    "weakness_paralysis as paralysis, " \
                    "weakness_blast as blast, " \
                    "weakness_stun  as stun "

ALT_RESIST_SQL = "select " \
                 "alt_weakness_fire as fire, " \
                 "alt_weakness_water as water, " \
                 "alt_weakness_thunder as thunder, " \
                 "alt_weakness_ice as ice, " \
                 "alt_weakness_dragon as dragon "

TRIBAL_IMAGE = "https://raw.githubusercontent.com/gatheringhallstudios/MHWorldData/master/images/monster/{}.png"


def getFormattedMonsterOutput(monsterName):
    officialName = getOfficialMonsterName(monsterName)
    return "{}\n{}".format(
            getMonsterImageUrl(
                    getId(officialName)),
            beautifyList(
                    mergeResistances(
                            getNormalResistances(officialName),
                            getAltResistances(officialName))))


def getOfficialMonsterName(monsterName):
    shorthandDict = yaml.load(open("settings/monsterShorthand.yml"))
    for monster in shorthandDict:
        if monsterName.lower() in [shorthand.lower() for shorthand in shorthandDict[monster]]:
            monsterName = monster
            break
    return monsterName.lower()


def getId(officialName):
    return getDatabaseConnection().execute(ID, [officialName]).fetchone()[0]


def getMonsterImageUrl(id1):
    return TRIBAL_IMAGE.format(id1)


def queryByMonsterName(sql, officialName):
    return getDatabaseConnection().execute(sql + FROM_MONSTER_BY_NAME, {"monsterName": officialName})


def getNormalResistances(officialName):
    query = queryByMonsterName(NORMAL_RESIST_SQL, officialName)
    results = query.fetchone()
    return {query.description[x][0]: results[x] for x in range(len(query.description))}


def getAltResistances(officialName):
    if not hasAltResistances(officialName):
        return {}
    query = queryByMonsterName(ALT_RESIST_SQL, officialName)
    results = query.fetchone()
    return {query.description[x][0]: results[x] for x in range(len(query.description))}


def mergeResistances(normalResistances, altResistances):
    if altResistances == {}:
        pass
    output = []
    for key, normal in normalResistances.items():
        if key in altResistances:
            output.append("{}: {} ({})".format(
                    key,
                    starsForValue(normal),
                    starsForValue(altResistances[key])))
        else:
            output.append("{}: {}".format(key, starsForValue(normal)))
    return output


def hasAltResistances(officialName):
    return queryByMonsterName("select has_alt_weakness ", officialName).fetchone()[0]


def starsForValue(value):
    stars = ""
    for x in range(value):
        stars += "\*"
    stars = handleImmune(stars)
    return stars


def handleImmune(stars):
    return "X" if stars == "" else stars
