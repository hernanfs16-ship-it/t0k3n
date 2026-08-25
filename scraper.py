import json
import re
from pathlib import Path

import json5
from curl_cffi import requests

URL = "https://bestleague.life/tok.html"
OUTPUT = Path("tokens.json")


def extract_mt_literal(html: str) -> str:
    declaration = re.search(r"\bvar\s+mt\s*=", html, re.IGNORECASE)

    if not declaration:
        raise ValueError("No se encontró la variable 'var mt'.")

    start = html.find("[", declaration.end())

    if start == -1:
        raise ValueError("No se encontró el inicio del array mt.")

    depth = 0
    quote = None
    escaped = False

    for index in range(start, len(html)):
        char = html[index]

        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in ('"', "'", "`"):
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1

            if depth == 0:
                return html[start:index + 1]

    raise ValueError("El array mt quedó sin cerrar.")


def extract_mt_variable():
    print(f"Conectando a {URL}...")

    response = requests.get(URL, impersonate="chrome", timeout=30)
    response.raise_for_status()

    mt_literal = extract_mt_literal(response.text)
    mt_data = json5.loads(mt_literal)

    # Convierte los datos a texto y elimina SOLO los [ ] externos.
    contenido = json.dumps(mt_data, ensure_ascii=False, indent=2)
    contenido_sin_corchetes = contenido[1:-1].strip()

    OUTPUT.write_text(
        contenido_sin_corchetes + "\n",
        encoding="utf-8",
    )

    print(f"Éxito: se guardaron {len(mt_data)} elementos en {OUTPUT}.")


if __name__ == "__main__":
    extract_mt_variable()
