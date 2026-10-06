#!/usr/bin/env python3

import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


SOURCE_EPG_URL = (
    "http://5.161.119.253/"
    "Immunity3-Viewing5-Extruding3-Fructose7-Steam4-Bloating8-"
    "Roman8-Remedial5-Frays5/epg.xml"
)

OUTPUT = Path("public/epg.xml")


TAQUILLAS = {
    "83278": "Taquilla Acción",
    "83283": "Taquilla Animación",
    "83281": "Taquilla Aventura",
    "83274": "Taquilla Ciencia Ficción",
    "150880": "Taquilla Cine España",
    "83277": "Taquilla Comedia",
    "150879": "Taquilla Documental",
    "83280": "Taquilla Drama",
    "83282": "Taquilla Fantasía",
    "83285": "Taquilla Histórica",
    "83279": "Taquilla Romance",
    "83284": "Taquilla Suspense",
    "83276": "Taquilla Terror",
    "83275": "Taquilla Western",
}


print("Descargando EPG externo...")

request = urllib.request.Request(
    SOURCE_EPG_URL,
    headers={
        "User-Agent": "Mozilla/5.0 SpinningTV-EPG/1.0"
    }
)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()

except Exception as error:
    sys.exit(f"Error descargando el EPG: {error}")


if not data:
    sys.exit("El servidor devolvió un EPG vacío.")


try:
    source_root = ET.fromstring(data)

except ET.ParseError as error:
    sys.exit(f"El XML recibido no es válido: {error}")


target_root = ET.Element(
    "tv",
    {
        "generator-info-name": "SpinningTV Taquillas EPG",
        "source-info-name": "EPG Taquillas"
    }
)


# --------------------------------------------------
# CANALES
# --------------------------------------------------

source_channels = {}

for channel in source_root.findall("channel"):

    channel_id = channel.get("id", "")

    if channel_id not in TAQUILLAS:
        continue

    if channel_id not in source_channels:
        source_channels[channel_id] = channel


for channel_id, channel_name in TAQUILLAS.items():

    new_channel = ET.SubElement(
        target_root,
        "channel",
        {"id": channel_id}
    )

    ET.SubElement(
        new_channel,
        "display-name"
    ).text = channel_name

    source_channel = source_channels.get(channel_id)

    if source_channel is not None:

        icon = source_channel.find("icon")

        if icon is not None and icon.get("src"):

            ET.SubElement(
                new_channel,
                "icon",
                {"src": icon.get("src")}
            )


# --------------------------------------------------
# PROGRAMACIÓN
# --------------------------------------------------

programme_count = 0

programme_by_channel = {
    channel_id: 0
    for channel_id in TAQUILLAS
}


for programme in source_root.findall("programme"):

    channel_id = programme.get("channel", "")

    if channel_id not in TAQUILLAS:
        continue

    target_root.append(programme)

    programme_count += 1
    programme_by_channel[channel_id] += 1


print("")
print("Programas encontrados:")

for channel_id, channel_name in TAQUILLAS.items():

    count = programme_by_channel[channel_id]

    print(
        f"{channel_name}: {count}"
    )


if programme_count == 0:

    sys.exit(
        "No se encontró ninguna programación "
        "para las 14 taquillas."
    )


# --------------------------------------------------
# GUARDAR XML
# --------------------------------------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)


tree = ET.ElementTree(target_root)


try:
    ET.indent(
        tree,
        space="  "
    )

except AttributeError:
    pass


tree.write(
    OUTPUT,
    encoding="utf-8",
    xml_declaration=True
)


print("")
print(
    f"EPG generado correctamente."
)

print(
    f"Canales: {len(TAQUILLAS)}"
)

print(
    f"Programas: {programme_count}"
)

print(
    f"Archivo: {OUTPUT}"
)
