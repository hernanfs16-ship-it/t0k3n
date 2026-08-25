import json
import re
from curl_cffi import requests

URL = "https://bestleague.life/tok.html"

def extract_mt_variable():
    try:
        print(f"Conectando a {URL} simulando ser Chrome...")
        
        # Usamos curl_cffi para imitar perfectamente la huella de Google Chrome
        response = requests.get(URL, impersonate="chrome", timeout=15)
        response.raise_for_status()
        html_content = response.text

        print(f"Página descargada. Inicio del HTML: {html_content[:150]}...")

        # Expresión regular para buscar la variable
        pattern = r"var\s+mt\s*=\s*(\[.*?\]);"
        match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)

        if match:
            json_str = match.group(1)
            mt_data = json.loads(json_str)

            with open("tokens.json", "w", encoding="utf-8") as f:
                json.dump(mt_data, f, indent=2, ensure_ascii=False)

            print(f"Éxito: Se extrajeron {len(mt_data)} elementos y se guardaron en tokens.json")
        else:
            print("Error: No se encontró la variable 'var mt' en el código fuente.")

    except Exception as e:
        print(f"Error al procesar la página: {e}")

if __name__ == "__main__":
    extract_mt_variable()
