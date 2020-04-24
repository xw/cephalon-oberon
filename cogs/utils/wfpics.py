def get_faction_pic(faction):
    faction = faction.lower()
    if "grineer" in faction:
        return "https://i.imgur.com/uNP3lcz.png"
    elif "corpus" in faction:
        return "https://i.imgur.com/tUcpeoH.png"
    elif "infested" in faction:
        return "https://i.imgur.com/8V4Nc7B.png"
    elif "sentient" in faction:
        return "https://i.imgur.com/kEbTLv5.png"
    else:
        return "https://i.imgur.com/m4VCiAt.png"

def get_boss_pic(boss):
    boss = boss.lower()
    if "alad" in boss:
        return "https://i.imgur.com/4Rv8CS2.png"
    elif "ambulas" in boss:
        return "https://i.imgur.com/clwDWbi.png"
    elif "hyena" in boss:
        return "https://i.imgur.com/n8ygJ0r.png"
    elif "jackal" in boss:
        return "https://i.imgur.com/2o2tW8Q.png"
    elif "kela" in boss:
        return "https://i.imgur.com/nbUiHCf.png"
    elif "kril" in boss:
        return "https://i.imgur.com/MxdUuNr.png"
    elif "lephantis" in boss:
        return "https://i.imgur.com/sqhQxBr.png"
    elif "phorid" in boss:
        return "https://i.imgur.com/0Rjt44R.png"
    elif "raptor" in boss:
        return "https://i.imgur.com/QD3DgZi.png"
    elif "sargas" in boss:
        return "https://i.imgur.com/he8LgBl.png"
    elif "sergeant" in boss:
        return "https://i.imgur.com/qPK5zer.png"
    elif "regor" in boss:
        return "https://i.imgur.com/aNVqefY.png"
    elif "hek" in boss:
        return "https://i.imgur.com/GISbfHD.png"
    elif "vor" in boss:
        return "https://i.imgur.com/0HXNfWF.png"
    else:
        return "https://i.imgur.com/OI4dnlc.png"
