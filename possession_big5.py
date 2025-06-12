import pandas as pd
import time
import re
import unidecode
import os

# Usamos un diccionario para asociar cada grupo de URLs con su respectiva liga.
leagues_urls = {
    "Big5": ["https://fbref.com/en/comps/Big5/possession/players/Big-5-European-Leagues-Stats"]
}

# --- CONFIGURACIÓN PARA EXPORTAR ---
output_dir = './data'
output_filename = 'possession_big5.csv'
output_path = os.path.join(output_dir, output_filename)

# Crear el directorio si no existe
os.makedirs(output_dir, exist_ok=True)

# Si el archivo ya existe, lo eliminamos para empezar de cero en cada ejecución.
if os.path.exists(output_path):
    os.remove(output_path)

dfs = []

# --- BUCLE PRINCIPAL MODIFICADO ---
# Iteramos sobre el diccionario de ligas y URLs
for league, urls in leagues_urls.items():
    for url in urls:
        try:
            df_list = pd.read_html(url)
            df = df_list[0]

            squad_name_match = re.search(r'/squads/[^/]+/([^-]+(?:-[^-]+)*)-Stats', url)
            if squad_name_match:
                squad_name = squad_name_match.group(1).replace("-", " ")
            else:
                squad_name = "Unknown Squad"

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(0)
            if 'Matches' in df.columns:
                df = df.drop(columns='Matches')

            if 'Player' in df.columns:
                df.loc[:, 'Player'] = df['Player'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
            if 'Squad' in df.columns:
                df.loc[:, 'Squad'] = df['Squad'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)

            if 'Player' in df.columns and 'Squad' in df.columns:
                df.loc[:, 'PlSqu'] = df['Player'].astype(str) + df['Squad'].astype(str)

            dfs.append(df)
            print(f"Procesado: {squad_name} ({league})")
        except Exception as e:
            print(f"Error con {url}: {e}")
        time.sleep(6)

if dfs:
    passing_types_df = pd.concat(dfs, ignore_index=True)
    df_cleaned = passing_types_df[~passing_types_df['Player'].str.contains('Player|Squad Total', na=False)]
    
    # --- REORDENAR COLUMNAS (OPCIONAL PERO RECOMENDADO) ---
    # Colocar 'League' y 'Squad' al principio para mayor claridad.
    cols = ['Squad', 'Player'] + [col for col in df_cleaned.columns if col not in ['Squad', 'Player']]
    df_cleaned = df_cleaned[cols]

    df_cleaned.to_csv(
                output_path,
                index=False
            )
    print(f"\n¡Proceso completado! Archivo guardado en: {output_path}")
else:
    print("\nNo se pudo procesar ningún dato.")
