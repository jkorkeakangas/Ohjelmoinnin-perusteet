"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    # Pilkotaan kentät
    (varausnumero, varaaja, paiva, aika, tunnit, tuntihinta, maksettu, kohde, puhelin, sahkoposti) = varaus.split("|")    

    # Muutetaan tiedot

    varausnumero = int(varausnumero)
    paiva = datetime.strptime(paiva, "%Y-%m-%d").date()
    suomalainenPaiva = paiva.strftime("%d.%m.%Y")
    aika = datetime.strptime(aika, "%H:%M").time()
    suomalainenAika = aika.strftime("%H.%M")
    tuntimäärä = int(tunnit)
    tuntihinta = float(tuntihinta)
    kokonaishinta = tuntimäärä * tuntihinta
    maksettuTekstina = "Kyllä" if maksettu.strip() == "True" else "Ei"

    # Tulostetaan varaus konsoliin
    print(f"Varausnumero: {varausnumero}")
    print(f"Varaaja: {varaaja}")
    print(f"Päivämäärä: {suomalainenPaiva}")
    print(f"Aloitusaika: {suomalainenAika}")
    print(f"Tuntimäärä: {tuntimäärä}")
    print(f"Tuntihinta: {tuntihinta}")
    print(f"Kokonaishinta: {kokonaishinta:.2f} €")
    print(f"Maksettu: {maksettuTekstina}")
    print(f"Kohde: {kohde}")
    print(f"Puhelin: {puhelin}")
    print(f"Sähköposti: {sahkoposti}")

    # Kokeile näitä
    #print(varaus.split('|'))
    #varausId = varaus.split('|')[0]
    #print(varausId)
    #print(type(varausId))
    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    main()