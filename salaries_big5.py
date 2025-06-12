import pandas as pd
import re
import os

# Lista de enlaces de salarios
links = [
    'https://fbref.com/en/comps/20/wages/Bundesliga-Wages',
    'https://fbref.com/en/comps/9/wages/Premier-League-Wages',
    'https://fbref.com/en/comps/12/wages/La-Liga-Wages',
    'https://fbref.com/en/comps/13/wages/Ligue-1-Wages',
    'https://fbref.com/en/comps/11/wages/Serie-A-Wages'
]

def extract_euro_value(val):
    """Extrae el valor numérico en euros desde una cadena con formato '€ 123,456 (x)'."""
    if isinstance(val, str):
        match = re.search(r'€\s?([\d,]+)', val)
        if match:
            return int(match.group(1).replace(',', ''))
    return None

def process_wage_table(url):
    """Lee y limpia la tabla de salarios desde un enlace de FBref."""
    try:
        df = pd.read_html(url)[1]
        df['Weekly Wages'] = df['Weekly Wages'].apply(extract_euro_value)
        df['Annual Wages'] = df['Annual Wages'].apply(extract_euro_value)
        return df
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return None

# Procesamos todos los enlaces y descartamos resultados vacíos
dfs = [process_wage_table(url) for url in links]
dfs = [df for df in dfs if df is not None and not df.empty]

# Si hay datos válidos, los procesamos y guardamos
if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    df_final['PlSqu'] = df_final['Player'].astype(str) + df_final['Squad'].astype(str)

    # Ruta de salida
    output_dir = './data'
    output_filename = 'salaries_big5.csv'
    output_path = os.path.join(output_dir, output_filename)

    # Crear el directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Eliminar el archivo si ya existe
    if os.path.exists(output_path):
        os.remove(output_path)

    # Guardar CSV
    df_final.to_csv(output_path, index=False)
    print(f"\n¡Proceso completado! Archivo guardado en: {output_path}")
else:
    print("\nNo se pudo procesar ningún dato.")
