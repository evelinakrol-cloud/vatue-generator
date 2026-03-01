import xml.etree.ElementTree as ET
import re
import pandas as pd

def generuj_vatue(df, nazwa_pliku):

    tree = ET.parse("szablon_vatue.xml")
    root = tree.getroot()

    ns = {"ns": "http://crd.gov.pl/wzor/2020/07/03/9690/"}

    match = re.search(r"(\d{4})_(\d{2})", nazwa_pliku)
    rok = match.group(1)
    miesiac = str(int(match.group(2)))

    root.find("ns:Naglowek/ns:Rok", ns).text = rok
    root.find("ns:Naglowek/ns:Miesiac", ns).text = miesiac

    pozycje = root.find("ns:PozycjeSzczegolowe", ns)

    for child in list(pozycje):
        if "AlwaysShow" not in child.tag:
            pozycje.remove(child)

    sekcja = None

    for _, row in df.iterrows():

        tekst = str(row[0]).strip()

        if tekst == "Sprzedaż WDT":
            sekcja = "Grupa1"
            continue

        if tekst == "Zakup WNT":
            sekcja = "Grupa2"
            continue

        if tekst == "Eksport Usług":
            sekcja = "Grupa3"
            continue

        if pd.notna(row[0]) and pd.notna(row[2]) and sekcja:

            kraj = str(row[0])
            vat = str(row[1])
            kwota = str(round(row[2]))

            grupa = ET.SubElement(pozycje, sekcja)

            if sekcja == "Grupa1":
                ET.SubElement(grupa, "P_Da").text = kraj
                ET.SubElement(grupa, "P_Db").text = vat
                ET.SubElement(grupa, "P_Dc").text = kwota
                ET.SubElement(grupa, "P_Dd").text = "1"

            elif sekcja == "Grupa2":
                ET.SubElement(grupa, "P_Na").text = kraj
                ET.SubElement(grupa, "P_Nb").text = vat
                ET.SubElement(grupa, "P_Nc").text = kwota
                ET.SubElement(grupa, "P_Nd").text = "1"

            elif sekcja == "Grupa3":
                ET.SubElement(grupa, "P_Ua").text = kraj
                ET.SubElement(grupa, "P_Ub").text = vat
                ET.SubElement(grupa, "P_Uc").text = kwota

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)