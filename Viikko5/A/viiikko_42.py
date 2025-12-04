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


def tulosta_paivasumma(pvm: date, k1: float, k2: float, k3: float,
                       t1: float, t2: float, t3: float):
    """
    Tulostaa yhden päivän kulutus- ja tuotantoarvot siistissä taulukossa.
    Käytetty tasaajia määrittämään oikea kohta tulostukseen.
    """
    vp = viikon_paivat[pvm.weekday()]

    print(
        f"{vp:<12}  {pvm.day:02d}.{pvm.month:02d}.{pvm.year}   "
        f"{muotoile_kwh(k1):>6}  {muotoile_kwh(k2):>6}  {muotoile_kwh(k3):>6}       "
        f"{muotoile_kwh(t1):>6} {muotoile_kwh(t2):>6} {muotoile_kwh(t3):>6}"
    )


def main():
    """Ohjelman pääfunktio: lukee datan, kutsutaan funktiota laskemaan arvot,
    käytetään toistorakennetta käymään läpi sanakirja. Kutsutaan funktio, johon
    on määritelty paikat tulostukselle ja tulostetaan pohja arvojen kanssa."""
    viikko_data = lue_data("viikko42.csv")
    paivittaiset = laske_paivittaiset_summat(viikko_data)

    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    print("Päivä         Pvm           Kulutus [kWh]                 Tuotanto [kWh]")
    print("              (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    print("---------------------------------------------------------------------------")

    for pvm in sorted(paivittaiset.keys()):
        k1, k2, k3, t1, t2, t3 = paivittaiset[pvm]
        tulosta_paivasumma(pvm, k1, k2, k3, t1, t2, t3)


if __name__ == "__main__":
    main()
