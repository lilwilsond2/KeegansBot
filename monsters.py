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


def queryByMonsterName(sql, officialName):
    return getDatabaseConnection().execute(sql + FROM_MONSTER_BY_NAME, {"monsterName": officialName})


def getOfficialMonsterName(monsterName):
    shorthandDict = yaml.load(open("settings/monsterShorthand.yml"))
    for monster in shorthandDict:
        if monsterName.lower() in [shorthand.lower() for shorthand in shorthandDict[monster]]:
            monsterName = monster
            break
    return monsterName.lower()


def starsForValue(value):
    stars = ""
    for x in range(value):
        stars += "\*"
    stars = handleImmune(stars)
    return stars


def handleImmune(stars):
    return "X" if stars == "" else stars


class Monster:
    def __init__(self, name):
        self.officialName = getOfficialMonsterName(name)
        self.id = self.getId()
        self.icon = self.getMonsterImageUrl()
        self.normalResistances = self.getNormalResistances()
        self.altResistances = self.getAltResistances()

    def __str__(self):
        return "{}\n{}".format(
                self.icon,
                beautifyList(self.mergeResistances()))

    def getNormalResistances(self):
        query = queryByMonsterName(NORMAL_RESIST_SQL, self.officialName)
        results = query.fetchone()
        return {query.description[x][0]: results[x] for x in range(len(query.description))}

    def getAltResistances(self):
        if not self.hasAltResistances():
            return {}
        query = queryByMonsterName(ALT_RESIST_SQL, self.officialName)
        results = query.fetchone()
        return {query.description[x][0]: results[x] for x in range(len(query.description))}

    def mergeResistances(self):
        if self.altResistances == {}:
            pass
        output = []
        for key, normal in self.normalResistances.items():
            if key in self.altResistances:
                output.append("{}: {} ({})".format(
                        key,
                        starsForValue(normal),
                        starsForValue(self.altResistances[key])))
            else:
                output.append("{}: {}".format(key, starsForValue(normal)))
        return output

    def getId(self):
        return getDatabaseConnection().execute(ID, [self.officialName]).fetchone()[0]

    def getMonsterImageUrl(self):
        return TRIBAL_IMAGE.format(self.id)

    def hasAltResistances(self):
        return queryByMonsterName("select has_alt_weakness ", self.officialName).fetchone()[0]
