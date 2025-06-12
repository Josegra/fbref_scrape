import pandas as pd
import time
import re
import unidecode
import os

# Usamos un diccionario para asociar cada grupo de URLs con su respectiva liga.
leagues_urls = {
    "Big5": ["https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"]
}

# --- CONFIGURACIÓN PARA EXPORTAR ---
output_dir = './data'
output_filename = 'standard_big5.csv'
output_path = os.path.join(output_dir, output_filename)

# Crear el directorio si no existe
os.makedirs(output_dir, exist_ok=True)

# Si el archivo ya existe, lo eliminamos para empezar de cero en cada ejecución.
if os.path.exists(output_path):
    os.remove(output_path)

dfs = []

def rename_duplicates_std(columns, target_col):
    count = 1
    new_columns = []
    for col_item in columns:
        if col_item == target_col:
            new_columns.append(f"{target_col}_{count}")
            count += 1
        else:
            new_columns.append(col_item)
    return new_columns

# Iteramos sobre el diccionario de ligas
for league, urls in leagues_urls.items():
    for url in urls:
        try:
            df_list = pd.read_html(url)
            # Se extrae la primera tabla (Índice 0) para "Standard Stats"
            df = df_list[0] 

            squad_name_match = re.search(r'/squads/[^/]+/([^-]+(?:-[^-]+)*)-Stats', url)
            if squad_name_match:
                squad_name = squad_name_match.group(1).replace("-", " ")
            else:
                squad_name = "Unknown Squad"

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(0)

            # --- INICIO DE REGLAS DE LIMPIEZA 
            if 'Matches' in df.columns:
                df = df.drop(columns='Matches')

            if 'Player' in df.columns:
                df.loc[:, 'Player'] = df['Player'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
            if 'Squad' in df.columns:
                df.loc[:, 'Squad'] = df['Squad'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)

            if 'Player' in df.columns and 'Squad' in df.columns:
                df.loc[:, 'PlSqu'] = df['Player'].astype(str) + df['Squad'].astype(str)

            # Renombrar columnas duplicadas (lógica específica para Standard Stats)
            for col_target in ['Gls', 'Ast', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR','xG', 'npxG', 'xA', 'npxG+xA', 'G+A', 'xAG', 'npxG+xAG']:
                if list(df.columns).count(col_target) > 1:
                    df.columns = rename_duplicates_std(df.columns, col_target)

            # Ajustar sufijos de columnas a _p90 (lógica específica para Standard Stats)
            new_cols = []
            for c in df.columns:
                if '_1' in c:
                    new_cols.append(c.replace('_1', ''))
                elif '_2' in c:
                    new_cols.append(c.replace('_2', '_p90'))
                elif c in ['G+A-PK', 'xG+xAG']:
                    new_cols.append(c + '_p90')
                else:
                    new_cols.append(c)
            df.columns = new_cols
            # --- FIN DE REGLAS DE LIMPIEZA ---

            dfs.append(df)
            print(f"Procesado: {squad_name} ({league})")
        except Exception as e:
            print(f"Error con {url}: {e}")
        # Mantenemos el tiempo de espera original del script
        time.sleep(5)

# Guardado del archivo final
if dfs:
    standard_df = pd.concat(dfs, ignore_index=True)
    df_cleaned = standard_df[~standard_df['Player'].str.contains('Player|Squad Total', na=False)]
    
    # Reordenar columnas para mejor visualización
    cols_to_front = ['Squad', 'Player', 'PlSqu']
    df_cleaned = df_cleaned[cols_to_front + [col for col in df_cleaned.columns if col not in cols_to_front]]
    
    df_cleaned.to_csv(output_path, index=False)
    print(f"\n¡Proceso completado! Archivo guardado en: {output_path}")
else:
    print("\nNo se pudo procesar ningún dato.")
