import re

def temizle_metin(metin):
    if not metin:
        return ""
    return metin.strip()


def bosluklari_koru(kaynak: str, hedef: str) -> str:
    if not kaynak or not hedef or not hedef.strip():
        return hedef

    bas_bosluk = re.match(r"^\s*", kaynak)
    son_bosluk = re.search(r"\s*$", kaynak)

    bas = bas_bosluk.group(0) if bas_bosluk else ""
    son = son_bosluk.group(0) if son_bosluk else ""

    return f"{bas}{hedef.strip()}{son}"
