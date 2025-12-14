# Copyright (c) 2025 Janne Korkeakangas
# This code is licensed under the MIT License.


from datetime import datetime, date

def muunna_tiedot(tiedot: list) -> list:
    """
    Muuttaa jokaisen annetun tietorivin tietotyypit oikeiksi.
    Pilkku korvataan pisteellä float-muunnosta varten.
    """
    return [
        datetime.fromisoformat(tiedot[0]),
        float(tiedot[1].replace(",", ".")),
        float(tiedot[2].replace(",", ".")),
        float(tiedot[3].replace(",", "."))
    ]

def muotoile_piste(arvo: float) -> str:
    """
    Muutetaan piste pilkuksi tämän funktion avulla, ja annetaan luku
    kahden desimaalin tarkkuudella.
    """
    return f"{arvo:.2f}".replace(".",",")


def lue_data(tiedoston_nimi: str) -> list:
    """
    Lukee CSV-tiedoston ja palauttaa rivit sopivassa rakenteessa ja tietotyypeissä.

    Kutsuu funktiota muunna_tiedot (lst):
     funktio palauttaa listan -> Tietotyypit muutettu

    Parametrit:
     tiedoston_nimi (str): ottaa vastaan tiedoston, jossa kentät jaettu merkillä ;

    Palautus:
     tietokanta (lst): palauttaa tietokannan, jossa tietotyypit on muutettu
    """
    tietokanta = []
    with open(tiedoston_nimi, "r", encoding="utf-8") as f:
        next(f)  # Otetaan kenttien esittelytiedot pois
        for tiedot in f:
            tiedot = tiedot.strip().split(";")
            tietokanta.append(muunna_tiedot(tiedot))

    return tietokanta


def raportti_tiedostoon(raportti: str):
    """
    Kirjoittaa annetun sisällön tiedostoon

    Parametrit:
     raportti (str): raporttiteksti
    """
    with open("raportti.txt", "w", encoding="utf-8") as f:
        f.write(raportti)


def raportti_aikavali(
    alku: datetime.date, loppu: datetime.date, tietokanta: list
) -> str:
    """
    Raporttiin tulostetaan aikaväliltä:
    * Alku- ja loppupäivä (pv.kk.vvvv-pv.kk.vvvv)
    * Aikavälin kokonaiskulutus (kWh, 2 desimaalia, pilkku desimaalina)
    * Aikavälin kokonaistuotanto (kWh, 2 desimaalia, pilkku desimaalina)
    * Aikavälin keskilämpötila (vuorokausilämpötilojen keskiarvo)

    Parametrit:
     raportti (str): raporttiteksti
    """
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti väliltä {alku.day}.{alku.month}.{alku.year}-"
    raportti += f"{loppu.day}.{loppu.month}.{loppu.year}\n"

    kulutus = 0
    tuotanto = 0
    paivien_lampotilat = {} 

    for rivi in tietokanta:
        pvm = rivi[0].date()

        if alku <= pvm <= loppu:
            kulutus += rivi[1]
            tuotanto += rivi[2]

            
            if pvm not in paivien_lampotilat:
                paivien_lampotilat[pvm] = rivi[3]

    if paivien_lampotilat:
        keskilampo = sum(paivien_lampotilat.values()) / len(paivien_lampotilat)
    else:
        keskilampo = 0

    raportti += f"- Kokonaiskulutus: {muotoile_piste(kulutus)} kWh\n"
    raportti += f"- Kokonaistuotanto: {muotoile_piste(tuotanto)} kWh\n"
    raportti += f"- Keskilämpötila: {muotoile_piste(keskilampo)} °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti

def raportti_kk(kuukausi: int, tietokanta: list) -> str:
    """
    Raporttiin tulostetaan:
    * Kuukausi
    * Kuukauden kokonaiskulutus (kWh)
    * Kuukauden kokonaistuotanto (kWh)
    * Kuukauden keskimääräinen vuorokauden lämpötila

    Parametrit:
     raportti (str): raporttiteksti
    """
    kuukaudet = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu", "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti kuulta: {kuukaudet[kuukausi-1]} \n"
    kulutus = 0
    tuotanto = 0
    paivien_lampotilat = {} 

    for rivi in tietokanta:
        pvm = rivi[0].date()

        if pvm.month == kuukausi:
            kulutus += rivi[1]
            tuotanto += rivi[2]

            if pvm not in paivien_lampotilat:
                paivien_lampotilat[pvm] = rivi[3]

    if paivien_lampotilat:
        keskilampo = sum(paivien_lampotilat.values()) / len(paivien_lampotilat)
    else:
        keskilampo = 0

    raportti += f"- Kokonaiskulutus: {muotoile_piste(kulutus)} kWh\n"
    raportti += f"- Kokonaistuotanto: {muotoile_piste(tuotanto)} kWh\n"
    raportti += f"- Keskilämpötila: {muotoile_piste(keskilampo)} °C\n"
    
    raportti += "-----------------------------------------------------\n"
    return raportti

def raportti_vuosi(tietokanta: list) -> str:
    """
    Raporttiin tulostetaan:
    * Koko vuosi
    * Vuoden kokonaiskulutus (kWh)
    * Vuoden kokonaistuotanto (kWh)
    * Vuoden keskimääräinen vuorokauden lämpötila

    Parametrit:
     raportti (str): raporttiteksti
    """
    raportti = "-----------------------------------------------------\n"
    raportti += f"Raportti vuodelta: {tietokanta[0][0].date().year} \n"

    kulutus = 0
    tuotanto = 0
    paivien_lampotilat = {} 

    for rivi in tietokanta:
        pvm = rivi[0].date()

        kulutus += rivi[1]
        tuotanto += rivi[2]

        if pvm not in paivien_lampotilat:
            paivien_lampotilat[pvm] = rivi[3]

    if paivien_lampotilat:
        keskilampo = sum(paivien_lampotilat.values()) / len(paivien_lampotilat)
    else:
        keskilampo = 0

    raportti += f"- Kokonaiskulutus: {muotoile_piste(kulutus)} kWh\n"
    raportti += f"- Kokonaistuotanto: {muotoile_piste(tuotanto)} kWh\n"
    raportti += f"- Keskilämpötila: {muotoile_piste(keskilampo)} °C\n"
    raportti += "-----------------------------------------------------\n"
    return raportti

def valikot(paavalikko: bool, alavalikko: bool) -> list:
    """
    Generoi valikot ja palauttaa valinnat listana

    Parametrit:
     paavalikko (bool): käynnistetäänkö päävalikko
     alavalikko (bool): käynnistetäänkö alavalikko

    Palautus:
     valikon_valinnat (str): Valikon valinta yhdistettyinä arvoihin
    """

    while True and paavalikko:
        print("-----------------------------------------------------")
        print("Valitse raporttityyppi:")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle")
        print("3) Vuoden 2025 kokonaisyhteenveto")
        print("4) Lopeta ohjelma")
        print("-----------------------------------------------------")
        try:
            valinta = int(input("Anna valinta (numero 1-4): "))
            if not (1 <= valinta <= 4):
                raise ValueError
        except:
            print("Valinta ei ole hyväksytty. Anna numero välillä 1-4.")
            continue

        if valinta == 1:
            try:
                alku = input("Anna alkupäivä (pv.kk.vvvv): ").split(".")
                loppu = input("Anna loppupäivä (pv.kk.vvvv): ").split(".")
                valinnat = [
                    0,
                    1,
                    date(int(alku[2]), int(alku[1]), int(alku[0])),
                    date(int(loppu[2]), int(loppu[1]), int(loppu[0])),
                ]
                break
            except:
                print(
                    "Valinta ei ole hyväksytty. Anna päivät muodossa pv.kk.vvvv. Palataan alkuun."
                )
                continue

        elif valinta == 2:
            try:
                kuukausi = int(input("Anna kuukauden numero (1–12): "))
                valinnat = [0, 2, kuukausi]
                break
            except:
                print(
                    "Valinta ei ole hyväksytty. Anna numero välillä 1-12. Palataan alkuun."
                )
                continue

        elif valinta == 3:
            valinnat = [0, 3]
            break
        elif valinta == 4:
            valinnat = [0, 4]
            break
        else:
            continue

    while True and alavalikko:
        print("-----------------------------------------------------")
        print("Mitä haluat tehdä seuraavaksi?")
        print("1) Kirjoita raportti tiedostoon raportti.txt")
        print("2) Luo uusi raportti")
        print("3) Lopeta")
        print("-----------------------------------------------------")
        try:
            valinta = int(input("Anna valinta (numero 1-3): "))
            if not (1 <= valinta <= 3):
                raise ValueError
        except:
            print("Valinta ei ole hyväksytty. Anna numero välillä 1-3.")
            continue

        valinnat = [1, valinta]
        break

    return valinnat


def main():
    """
    Ohjelman pääfunktio: kysyys käyttäjältä inputteja ja tulostaa/vie tiedostoon raportteja
    """
    # Luetaan data tiedostosta
    kulutusTuotanto2025 = lue_data("2025.csv")

    while True:
        paavalikko = valikot(True, False)
        if paavalikko[1] == 1:
            raportti = raportti_aikavali(paavalikko[2], paavalikko[3], kulutusTuotanto2025)
            print(raportti)
        elif paavalikko[1] == 2:
            raportti = raportti_kk(paavalikko[2], kulutusTuotanto2025)
            print(raportti)
        elif paavalikko[1] == 3:
            raportti = raportti_vuosi(kulutusTuotanto2025)
            print(raportti)
        elif paavalikko[1] == 4:
            break

        alavalikko = valikot(False, True)
        if alavalikko[1] == 1:
            raportti_tiedostoon(raportti)
            continue
        elif alavalikko[1] == 2:
            continue
        elif alavalikko[1] == 3:
            break


if __name__ == "__main__":
    main()