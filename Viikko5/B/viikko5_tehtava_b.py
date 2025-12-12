# Copyright (c) 2025 Janne Korkeakangas
# License: MIT

from datetime import datetime, date
from typing import List, Dict


def muunna_tiedot(kulutus_tuotanto_tieto: List[str]) -> List:
    """
    Muutetaan yksittäisten tietojen datatyyppi.
    """
    muutettu_tieto = []
    muutettu_tieto.append(datetime.fromisoformat(kulutus_tuotanto_tieto[0]))
    muutettu_tieto.append(int(kulutus_tuotanto_tieto[1]))
    muutettu_tieto.append(int(kulutus_tuotanto_tieto[2]))
    muutettu_tieto.append(int(kulutus_tuotanto_tieto[3]))
    muutettu_tieto.append(int(kulutus_tuotanto_tieto[4]))
    muutettu_tieto.append(int(kulutus_tuotanto_tieto[5]))
    muutettu_tieto.append(int(kulutus_tuotanto_tieto[6]))
    return muutettu_tieto


def lue_data(tiedoston_nimi: str) -> List[list]:
    """
    Lukee CSV-tiedoston ja luo taulukkorakenteen.
    """
    kulutus_tuotanto_tiedot = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)
        for kulutus_tuotanto_tieto in f:
            kulutus_tuotanto_tieto = kulutus_tuotanto_tieto.strip()
            sarakkeet = kulutus_tuotanto_tieto.split(';')
            kulutus_tuotanto_tiedot.append(muunna_tiedot(sarakkeet))
    return kulutus_tuotanto_tiedot


viikon_paivat = [
    "maanantai", "tiistai", "keskiviikko",
    "torstai", "perjantai", "lauantai", "sunnuntai"
]


def muotoile_kwh(arvo: float) -> str:
    """
    Muutetaan piste pilkuksi tämän funktion avulla, ja annetaan luku
    kahden desimaalin tarkkuudella.
    """
    return f"{arvo:.2f}".replace(".", ",")


def laske_paivittaiset_summat(data: List[list]) -> Dict[date, List[float]]:
    """
    Laskee päiväkohtaisen kulutuksen ja tuotannon,ja luodaan sanakirja 
    päivästä ja sille annetaan kuusi arvoa, jotka muutetaan kwh
    jakamalla 1000. Annetaan 0 arvo jokaiselle arvolle, jotta
    ei tapahdu virheitä uusien päivien kohdalla. Tuohon arvoon lisätään
    kyseisen päivän oikea kulutus- tai tuotantoarvo-
    """
    paiva_summat: Dict[date, List[float]] = {}

    for rivi in data:
        aikaleima = rivi[0]
        pvm = aikaleima.date()

        k1 = rivi[1] / 1000
        k2 = rivi[2] / 1000
        k3 = rivi[3] / 1000
        t1 = rivi[4] / 1000
        t2 = rivi[5] / 1000
        t3 = rivi[6] / 1000

        if pvm not in paiva_summat:
            paiva_summat[pvm] = [0, 0, 0, 0, 0, 0]

        paiva_summat[pvm][0] += k1
        paiva_summat[pvm][1] += k2
        paiva_summat[pvm][2] += k3
        paiva_summat[pvm][3] += t1
        paiva_summat[pvm][4] += t2
        paiva_summat[pvm][5] += t3

    return paiva_summat



def muodosta_paivarivi(pvm: date, summat: List[float]) -> str:
    """
    Luodaan ulkoasu yhtä riviä varten.
    """
    k1, k2, k3, t1, t2, t3 = summat
    vp = viikon_paivat[pvm.weekday()]
    return (
        f"{vp:<12}  {pvm.day:02d}.{pvm.month:02d}.{pvm.year}   "
        f"{muotoile_kwh(k1):>6}  {muotoile_kwh(k2):>6}  {muotoile_kwh(k3):>6}       "
        f"{muotoile_kwh(t1):>6} {muotoile_kwh(t2):>6} {muotoile_kwh(t3):>6}"
    )


def kirjoita_raportti(raporttiteksti: str):
    """
    Kirjoittaa raportin tiedostoon yhteenveto.txt.
    """
    with open("yhteenveto.txt", "w", encoding="utf-8") as f:
        f.write(raporttiteksti)


def muodosta_viikkoraportti(viikko_numero: int, paivittaiset: Dict[date, List[float]]) -> str:
    """
    Luo yhden viikon raporttiosuuden tekstinä.
    """
    viikkoraporttirivit = []
    viikkoraporttirivit.append(f"Viikon {viikko_numero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    viikkoraporttirivit.append("Päivä         Pvm           Kulutus [kWh]                 Tuotanto [kWh]")
    viikkoraporttirivit.append("              (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    viikkoraporttirivit.append("---------------------------------------------------------------------------")

    for pvm in sorted(paivittaiset.keys()):
        viikkoraporttirivit.append(muodosta_paivarivi(pvm, paivittaiset[pvm]))

    viikkoraporttirivit.append("\n\n")
    return "\n".join(viikkoraporttirivit)


def main():
    """
    Ohjelman pääfunktio: käydään viikot läpi silmukalla. Lasketaan datan sisältämät summat,
    määritellään raportin sisältö ja muodostetaan niistä viikottaiset raporttitekstit
    Lopuksi kaikki kirjoitetaan yhteen tiedostoon yhteenveto.txt.
    """
    raportti = []

    for viikko, tiedosto in [
        (41, "viikko41.csv"),
        (42, "viikko42.csv"),
        (43, "viikko43.csv")
    ]:
        data = lue_data(tiedosto)
        paivittaiset = laske_paivittaiset_summat(data)
        raportti.append(muodosta_viikkoraportti(viikko, paivittaiset))

    kirjoita_raportti("\n".join(raportti))


if __name__ == "__main__":
    main()