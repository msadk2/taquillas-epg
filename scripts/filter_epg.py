#!/usr/bin/env python3

import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


BASE_URL = os.getenv("XUI_BASE_URL", "https://flexgo.xyz:443").rstrip("/")
USERNAME = os.getenv("XUI_USERNAME", "").strip()
PASSWORD = os.getenv("XUI_PASSWORD", "").strip()

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


if not USERNAME or not PASSWORD:
    sys.exit("Faltan XUI_USERNAME y/o XUI_PASSWORD en los Secrets de GitHub.")


params = urllib.parse.urlencode({
    "username": USERNAME,
    "password": PASSWORD
})

url = f"{BASE_URL}/xmltv.php?{params}"

print("Descargando EPG completo de XUI...")

request = urllib.request.Request(
    url,
    headers={"User-Agent": "SpinningTV-EPG/1.0"}
)

with urllib.request.urlopen(request, timeout=90) as response:
    data = response.read()


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
        "source-info-name": "XUI.one"
    }
)


selected_channels = {}


for channel in source_root.findall("channel"):

    channel_id = channel.get("id", "")

    if channel_id not in TAQUILLAS:
        continue

    expected_name = TAQUILLAS[channel_id].casefold()

    display_name = (
        channel.findtext("display-name") or ""
    ).strip()

    if channel_id not in selected_channels:
        selected_channels[channel_id] = channel

    if display_name.casefold() == expected_name:
        selected_channels[channel_id] = channel


for channel_id, expected_name in TAQUILLAS.items():

    source_channel = selected_channels.get(channel_id)

    new_channel = ET.SubElement(
        target_root,
        "channel",
        {"id": channel_id}
    )

    ET.SubElement(
        new_channel,
        "display-name"
    ).text = expected_name

    if source_channel is not None:

        icon = source_channel.find("icon")

        if icon is not None and icon.get("src"):

            ET.SubElement(
                new_channel,
                "icon",
                {"src": icon.get("src")}
            )


programme_count = 0


for programme in source_root.findall("programme"):

    channel_id = programme.get("channel", "")

    if channel_id not in TAQUILLAS:
        continue

    target_root.append(programme)

    programme_count += 1


if programme_count == 0:

    sys.exit(
        "No se encontró programación para las 14 taquillas. "
        "No se genera el EPG."
    )


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)


tree = ET.ElementTree(target_root)


try:
    ET.indent(tree, space="  ")
except AttributeError:
    pass


tree.write(
    OUTPUT,
    encoding="utf-8",
    xml_declaration=True
)


print(
    f"EPG generado correctamente: "
    f"{len(TAQUILLAS)} canales y "
    f"{programme_count} programas."
)
