"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus):
    numero = varaus[0]
    print(f"Varausnumero: {numero}")

def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def hae_paiva(varaus):
    ap_paiva = varaus[2]
    try:
        paiva = datetime.strptime(ap_paiva, "%Y-%m-%d").date()
        suomalainen_paiva = paiva.strftime("%d.%m.%Y")
    except ValueError:
        suomalainen_paiva = ap_paiva
    print(f"Päivämäärä: {suomalainen_paiva}")

def hae_aloitusaika(varaus):
    ap_aika = varaus[3]
    try:
        aika = datetime.strptime(ap_aika, "%H:%M").time()
        suomalainen_aika = aika.strftime("%H.%M")
    except ValueError:
        suomalainen_aika = ap_aika
    print(f"Aloitusaika: {suomalainen_aika}")

def hae_tuntimaara(varaus):
    tm = varaus[4]
    print(f"Tuntimäärä: {tm}")

def hae_tuntihinta(varaus):
    th = float(varaus[5].replace(',', '.'))
    hinta = str(f"{th:.2f}").replace('.', ',')
    print(f"Tuntihinta: {hinta} €")
    return th

def laske_kokonaishinta(varaus):
    tm = int(varaus[4].strip())
    th = float(varaus[5].replace(',', '.'))
    kh = tm * th
    kokonaishinta = str(f"{kh:.2f}").replace('.', ',')
    print(f"Kokonaishinta: {kokonaishinta} €")


def hae_maksettu(varaus):
    maksettu = varaus[6].strip()

    if maksettu.lower() in ["true", "1", "kylla", "k"]:
        maksettu = "Kyllä"
    elif maksettu.lower() in ["false", "0", "ei", "e"]:
        maksettu = "Ei"
    print(f"Maksettu: {maksettu}")

def hae_kohde(varaus):
    kohde = varaus[7]
    print(f"Kohde: {kohde}")

def hae_puhelin(varaus):
    puh = varaus[8]
    print(f"Puhelin: {puh}")

def hae_sahkoposti(varaus):
    sp = varaus[9]
    print(f"Sähköposti: {sp}")

    

def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        varaus = varaus.split('|')

    # Toteuta loput funktio hae_varaaja(varaus) mukaisesti
    # Luotavat funktiota tekevat tietotyyppien muunnoksen
    # ja tulostavat esimerkkitulosteen mukaisesti

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)

if __name__ == "__main__":
    main()