import json
import re
import requests

# REEMPLAZA ESTA URL POR LA PÁGINA REAL
URL = "https://bestleague.life/tok.html"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def extract_mt_variable():
    try:
        print(f"Conectando a {URL}...")
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()
        html_content = response.text

        # Expresión regular para capturar el contenido del array var mt = [ ... ];
        pattern = r"var\s+mt\s*=\s*(\[\s*\{.*?\}\s*\]);"
        match = re.search(pattern, html_content, re.DOTALL)

        if match:
            json_str = match.group(1)
            # Convertir el string extraído a un objeto Python
            mt_data = json.loads(json_str)

            # Guardar los datos en un archivo JSON local
            with open("tokens.json", "w", encoding="utf-8") as f:
                json.dump(mt_data, f, indent=2, ensure_ascii=False)

            print(f"Éxito: Se extrajeron {len(mt_data)} elementos y se guardaron en tokens.json")
        else:
            print("No se encontró la variable 'var mt' en el código fuente de la página.")

    except Exception as e:
        print(f"Error al procesar la página: {e}")

if __name__ == "__main__":
    extract_mt_variable()
