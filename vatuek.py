import xml.etree.ElementTree as ET
import re
import pandas as pd

def generuj_vatuek(df, nazwa_pliku):

    tree = ET.parse("szablon_vatuek.xml")
    root = tree.getroot()

    ns = {"ns": "http://crd.gov.pl/wzor/2020/07/03/9689/"}

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

        if pd.notna(row[0]) and pd.notna(row[2]) and pd.notna(row[3]) and sekcja:

            kraj = str(row[0])
            vat = str(row[1])
            bylo = str(round(row[2]))
            jest = str(round(row[3]))

            grupa = ET.SubElement(pozycje, sekcja)

            if sekcja == "Grupa1":

                ET.SubElement(grupa, "P_DBa").text = kraj
                ET.SubElement(grupa, "P_DBb").text = vat
                ET.SubElement(grupa, "P_DBc").text = bylo
                ET.SubElement(grupa, "P_DBd").text = "1"

                ET.SubElement(grupa, "P_DJa").text = kraj
                ET.SubElement(grupa, "P_DJb").text = vat
                ET.SubElement(grupa, "P_DJc").text = jest
                ET.SubElement(grupa, "P_DJd").text = "1"

            elif sekcja == "Grupa2":

                ET.SubElement(grupa, "P_NBa").text = kraj
                ET.SubElement(grupa, "P_NBb").text = vat
                ET.SubElement(grupa, "P_NBc").text = bylo
                ET.SubElement(grupa, "P_NBd").text = "1"

                ET.SubElement(grupa, "P_NJa").text = kraj
                ET.SubElement(grupa, "P_NJb").text = vat
                ET.SubElement(grupa, "P_NJc").text = jest
                ET.SubElement(grupa, "P_NJd").text = "1"

            elif sekcja == "Grupa3":

                ET.SubElement(grupa, "P_UBa").text = kraj
                ET.SubElement(grupa, "P_UBb").text = vat
                ET.SubElement(grupa, "P_UBc").text = bylo

                ET.SubElement(grupa, "P_UJa").text = kraj
                ET.SubElement(grupa, "P_UJb").text = vat
                ET.SubElement(grupa, "P_UJc").text = jest

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)