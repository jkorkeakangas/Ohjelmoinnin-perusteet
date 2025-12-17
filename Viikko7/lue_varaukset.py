# Copyright (c) 2025 Janne Korkeakangas
# License: MIT

from datetime import datetime


def muunna_varaustiedot(varaus: list) -> dict:
    return {
        "id": int(varaus[0]),
        "nimi": varaus[1],
        "sahkoposti": varaus[2],
        "puhelin": varaus[3],
        "paiva": datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus[5], "%H:%M").time(),
        "kesto": int(varaus[6]),
        "hinta": float(varaus[7]),
        "vahvistettu": varaus[8].lower() == "true",
        "kohde": varaus[9],
        "luotu": datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    }


def hae_varaukset(varaustiedosto: str) -> dict:
    varaukset = {}

    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            varaustiedot = rivi.strip().split("|")
            varaus = muunna_varaustiedot(varaustiedot)

            varaukset[varaus["id"]] = varaus

    return varaukset



def vahvistetut_varaukset(varaukset: dict):
    for varaus in varaukset.values():
        if varaus["vahvistettu"]:
            print(
                f"- {varaus['nimi']}, {varaus['kohde']}, "
                f"{varaus['paiva'].strftime('%d.%m.%Y')} "
                f"klo {varaus['kellonaika'].strftime('%H.%M')}"
            )
    print()



def pitkat_varaukset(varaukset: dict):
    for varaus in varaukset.values():
        if varaus["kesto"] >= 3:
            print(
                f"- {varaus['nimi']}, "
                f"{varaus['paiva'].strftime('%d.%m.%Y')} "
                f"klo {varaus['kellonaika'].strftime('%H.%M')}, "
                f"kesto {varaus['kesto']} h, {varaus['kohde']}"
            )
    print()



def varausten_vahvistusstatus(varaukset: dict):
    for varaus in varaukset.values():
        status = "Vahvistettu" if varaus["vahvistettu"] else "EI vahvistettu"
        print(f"{varaus['nimi']} → {status}")
    print()



def varausten_lkm(varaukset: dict):
    vahvistetut = 0
    ei_vahvistetut = 0

    for varaus in varaukset.values():
        if varaus["vahvistettu"]:
            vahvistetut += 1
        else:
            ei_vahvistetut += 1

    print(f"- Vahvistettuja varauksia: {vahvistetut} kpl")
    print(f"- Ei-vahvistettuja varauksia: {ei_vahvistetut} kpl")
    print()



def varausten_kokonaistulot(varaukset: dict):
    tulot = 0

    for varaus in varaukset.values():
        if varaus["vahvistettu"]:
            tulot += varaus["kesto"] * varaus["hinta"]

    print(
        "Vahvistettujen varausten kokonaistulot:",
        f"{tulot:.2f}".replace(".", ","),
        "€"
    )
    print()



def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()