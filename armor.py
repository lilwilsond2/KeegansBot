from helper import getJsonObjectsFromUrl, beautifyList


def armorLookup(skill: str) -> list:
    """
    Looks up armor pieces for a skill from mhw-db.com
    :param skill: skill to lookup
    :return: list of armor names
    """
    apiObjects = getArmors()
    output = filterArmors(apiObjects, skill)
    return output


def filterArmors(apiObjects, skill) -> list:
    filteredArmor = []
    for armorPiece in apiObjects:
        for armorSkill in armorPiece['skills']:
            if armorSkill['skillName'].lower() == skill.lower():
                filteredArmor.append(armorPiece)
    output = [armorPiece['name'] for armorPiece in filteredArmor]
    output.sort()
    return output


def getFormattedArmorOutput(skill):
    armorPieces = armorLookup(skill)
    output = beautifyList(armorPieces)
    return output


def getArmors():
    requestUrl = "https://mhw-db.com/armor?p={\"name\": true, \"skills.skillName\": true, \"skills.level\": true}"
    return getJsonObjectsFromUrl(requestUrl)
