import json
import re
import cloudscraper

URL = "https://bestleague.life/tok.html"

def extract_mt_variable():
    try:
        print(f"Conectando a {URL} con cloudscraper...")
        
        # Usamos cloudscraper en lugar de requests para evadir bloqueos antibot
        scraper = cloudscraper.create_scraper()
        response = scraper.get(URL, timeout=15)
        response.raise_for_status()
        html_content = response.text

        # Imprimimos un fragmento para confirmar qué respondió la página
        print(f"Página descargada. Inicio del HTML: {html_content[:150]}...")

        # Expresión regular ajustada para capturar el contenido del array
        pattern = r"var\s+mt\s*=\s*(\[.*?\]);"
        match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)

        if match:
            json_str = match.group(1)
            # Convertir el string extraído a un objeto Python
            mt_data = json.loads(json_str)

            # Guardar los datos en un archivo JSON local
            with open("tokens.json", "w", encoding="utf-8") as f:
                json.dump(mt_data, f, indent=2, ensure_ascii=False)

            print(f"Éxito: Se extrajeron {len(mt_data)} elementos y se guardaron en tokens.json")
        else:
            print("Error: No se encontró la variable 'var mt' en el código fuente.")
            print("Es posible que la página siga bloqueando al bot o requiera JavaScript para cargar.")

    except Exception as e:
        print(f"Error al procesar la página: {e}")

if __name__ == "__main__":
    extract_mt_variable()
