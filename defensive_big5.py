import pandas as pd
import time
import re
import unidecode
import os

# Usamos un diccionario para asociar cada grupo de URLs con su respectiva liga.
leagues_urls = {
    "Big5": ["https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats"]
}

# --- CONFIGURACIÓN PARA EXPORTAR ---
output_dir = './data'
output_filename = 'defensive_big5.csv'
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
            # CAMBIO: Seleccionar la tabla de "Defensive Actions" (índice 7).
            df = df_list[0]

            squad_name_match = re.search(r'/squads/[^/]+/([^-]+(?:-[^-]+)*)-Stats', url)
            if squad_name_match:
                squad_name = squad_name_match.group(1).replace("-", " ")
            else:
                squad_name = "Unknown Squad"

            # --- LÓGICA DE RENOMBRAMIENTO DE COLUMNAS PARA ACCIONES DEFENSIVAS ---
            if isinstance(df.columns, pd.MultiIndex):
                new_cols = []
                for level0, level1 in df.columns:
                    # Columnas con encabezado superior descriptivo (Tackles, Challenges, Blocks)
                    if level0 in ['Tackles', 'Challenges', 'Blocks']:
                        # Usamos el encabezado superior como prefijo para crear nombres únicos
                        new_cols.append(f"{level0}_{level1}")
                    else:
                        # Columnas sin encabezado superior (Player, Nation, Int, etc.)
                        new_cols.append(level1)
                df.columns = new_cols
            # Eliminamos la columna 'Matches' que viene al final y no es necesaria
            if 'Matches' in df.columns:
                df = df.drop(columns='Matches')

            # Normalizamos texto en columnas clave
            if 'Player' in df.columns:
                df.loc[:, 'Player'] = df['Player'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
            if 'Squad' in df.columns:
                df.loc[:, 'Squad'] = df['Squad'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)

            # Creamos la clave única PlSqu
            if 'Player' in df.columns and 'Squad' in df.columns:
                df.loc[:, 'PlSqu'] = df['Player'].astype(str) + df['Squad'].astype(str)

            dfs.append(df)
            print(f"Procesado: {squad_name} ({league})")
        except Exception as e:
            print(f"Error con {url}: {e}")
        # Mantenemos la pausa para no sobrecargar el servidor
        time.sleep(6)

if dfs:
    # CAMBIO: Nombre del DataFrame combinado para mayor claridad.
    defensive_df = pd.concat(dfs, ignore_index=True)
    # Filtramos las filas de resumen que contienen "Player" o "Squad Total"
    df_cleaned = defensive_df[~defensive_df['Player'].str.contains('Player|Squad Total', na=False)]

    # --- REORDENAR COLUMNAS (OPCIONAL PERO RECOMENDADO) ---
    cols_to_order = ['Squad', 'Player']
    other_cols = [col for col in df_cleaned.columns if col not in cols_to_order and col != 'PlSqu']
    final_cols_order = cols_to_order + other_cols + ['PlSqu']
    df_cleaned = df_cleaned[final_cols_order]

    # Guardamos el archivo CSV final
    df_cleaned.to_csv(
        output_path,
        index=False
    )
    print(f"\n¡Proceso completado! Archivo guardado en: {output_path}")
else:
    print("\nNo se pudo procesar ningún dato.")
