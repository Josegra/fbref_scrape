import pandas as pd
import time
import re
import unidecode
import os

# -- ESTRUCTURA DE DATOS MEJORADA --
# Usamos un diccionario para asociar cada grupo de URLs con su respectiva liga.
leagues_urls = {
    "EFL Championship": [
        "https://fbref.com/en/squads/5bfb9659/Leeds-United-Stats", "https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats", "https://fbref.com/en/squads/943e8050/Burnley-Stats", "https://fbref.com/en/squads/8ef52968/Sunderland-Stats", "https://fbref.com/en/squads/f7e3dfe9/Coventry-City-Stats", "https://fbref.com/en/squads/93493607/Bristol-City-Stats", "https://fbref.com/en/squads/e090f40b/Blackburn-Rovers-Stats", "https://fbref.com/en/squads/e3c537a1/Millwall-Stats", "https://fbref.com/en/squads/60c6b05f/West-Bromwich-Albion-Stats", "https://fbref.com/en/squads/7f59c601/Middlesbrough-Stats", "https://fbref.com/en/squads/fb10988f/Swansea-City-Stats", "https://fbref.com/en/squads/bba7d733/Sheffield-Wednesday-Stats", "https://fbref.com/en/squads/1c781004/Norwich-City-Stats", "https://fbref.com/en/squads/2abfe087/Watford-Stats", "https://fbref.com/en/squads/a757999c/Queens-Park-Rangers-Stats", "https://fbref.com/en/squads/76ffc013/Portsmouth-Stats", "https://fbref.com/en/squads/604617a2/Oxford-United-Stats", "https://fbref.com/en/squads/17892952/Stoke-City-Stats", "https://fbref.com/en/squads/26ab47ee/Derby-County-Stats", "https://fbref.com/en/squads/22df8478/Preston-North-End-Stats", "https://fbref.com/en/squads/bd8769d1/Hull-City-Stats", "https://fbref.com/en/squads/e297cd13/Luton-Town-Stats", "https://fbref.com/en/squads/32a1480e/Plymouth-Argyle-Stats", "https://fbref.com/en/squads/75fae011/Cardiff-City-Stats"
    ],
    "Primeira Liga": [
        "https://fbref.com/en/squads/13dc44fd/Sporting-CP-Stats", "https://fbref.com/en/squads/a77c513e/2024-2025/Benfica-Stats", "https://fbref.com/en/squads/5e876ee6/2024-2025/Porto-Stats", "https://fbref.com/en/squads/69d84c29/Braga-Stats", "https://fbref.com/en/squads/f5b64cb1/Santa-Clara-Stats", "https://fbref.com/en/squads/3f319bc9/Vitoria-Guimaraes-Stats", "https://fbref.com/en/squads/2de656d5/Famalicao-Stats", "https://fbref.com/en/squads/00c41b75/Estoril-Stats", "https://fbref.com/en/squads/b20a2b76/Casa-Pia-Stats", "https://fbref.com/en/squads/e4502862/Moreirense-Stats", "https://fbref.com/en/squads/eea856da/Rio-Ave-Stats", "https://fbref.com/en/squads/0d36ddd4/Arouca-Stats", "https://fbref.com/en/squads/6a329209/Gil-Vicente-FC-Stats", "https://fbref.com/en/squads/5c9eb756/Nacional-Stats", "https://fbref.com/en/squads/0cb9f756/Estrela-Stats", "https://fbref.com/en/squads/e5ce5a65/AVS-Futebol-Stats", "https://fbref.com/en/squads/489c9cd9/Farense-Stats", "https://fbref.com/en/squads/37b7e9e2/Boavista-Stats"
    ],
    "Serie B": [
        "https://fbref.com/en/squads/e2befd26/Sassuolo-Stats", "https://fbref.com/en/squads/4cceedfc/Pisa-Stats", "https://fbref.com/en/squads/68449f6d/Spezia-Stats", "https://fbref.com/en/squads/9aad3a77/Cremonese-Stats", "https://fbref.com/en/squads/9144bbcf/Juve-Stabia-Stats", "https://fbref.com/en/squads/b964e6bb/Catanzaro-Stats", "https://fbref.com/en/squads/283f2557/Cesena-Stats", "https://fbref.com/en/squads/ee058a17/Palermo-Stats", "https://fbref.com/en/squads/01baa639/Bari-Stats", "https://fbref.com/en/squads/13dabbde/Sudtirol-Stats", "https://fbref.com/en/squads/71a3700b/Modena-Stats", "https://fbref.com/en/squads/379ce81a/Carrarese-Stats", "https://fbref.com/en/squads/19008e93/Reggiana-Stats", "https://fbref.com/en/squads/db80f322/Mantova-Stats", "https://fbref.com/en/squads/4ef57aeb/Brescia-Stats", "https://fbref.com/en/squads/6a7ad59d/Frosinone-Stats", "https://fbref.com/en/squads/c5577084/Salernitana-Stats", "https://fbref.com/en/squads/8ff9e3b3/Sampdoria-Stats", "https://fbref.com/en/squads/1a8d4355/Cittadella-Stats", "https://fbref.com/en/squads/34963d0d/Cosenza-Stats"
    ],
    "Liga MX": [
        "https://fbref.com/en/squads/632f1838/Cruz-Azul-Stats", "https://fbref.com/en/squads/44b88a4e/Toluca-Stats", "https://fbref.com/en/squads/d9e1bd51/UANL-Stats", "https://fbref.com/en/squads/18d3c3a3/2024-2025/America-Stats", "https://fbref.com/en/squads/dd5ca9bd/2024-2025/Monterrey-Stats", "https://fbref.com/en/squads/c9d59c6c/Pumas-UNAM-Stats", "https://fbref.com/en/squads/fd7dad55/Leon-Stats", "https://fbref.com/en/squads/5d274ee4/Atletico-Stats", "https://fbref.com/en/squads/a42ddf2f/Tijuana-Stats", "https://fbref.com/en/squads/c02b0f7a/Guadalajara-Stats", "https://fbref.com/en/squads/752db496/Necaxa-Stats", "https://fbref.com/en/squads/1be8d2e3/2024-2025/Pachuca-Stats", "https://fbref.com/en/squads/29bff345/FC-Juarez-Stats", "https://fbref.com/en/squads/7c76bc53/Atlas-Stats", "https://fbref.com/en/squads/c3352ce7/Queretaro-Stats", "https://fbref.com/en/squads/f0297c23/Mazatlan-Stats", "https://fbref.com/en/squads/73fd2313/Puebla-Stats", "https://fbref.com/en/squads/03b65ba9/Santos-Laguna-Stats"
    ],
    "Argentine Primera División": [
        "https://fbref.com/en/squads/87a920fa/Rosario-Central-Stats", "https://fbref.com/en/squads/d01a653b/Argentinos-Juniors-Stats", "https://fbref.com/en/squads/795ca75e/Boca-Juniors-Stats", "https://fbref.com/en/squads/ef99c78c/River-Plate-Stats", "https://fbref.com/en/squads/40bb0ce9/Independiente-Stats", "https://fbref.com/en/squads/8e20e13d/Racing-Club-Stats", "https://fbref.com/en/squads/1d3d37ae/Huracan-Stats", "https://fbref.com/en/squads/0e92bf17/Tigre-Stats", "https://fbref.com/en/squads/66da6009/San-Lorenzo-Stats", "https://fbref.com/en/squads/8a9d5afa/Independiente-Rivadavia-Stats", "https://fbref.com/en/squads/1d89634b/Barracas-Central-Stats", "https://fbref.com/en/squads/b3d222b1/Deportivo-Riestra-Stats", "https://fbref.com/en/squads/3cbfa767/Platense-Stats", "https://fbref.com/en/squads/df734df9/Estudiantes-LP-Stats", "https://fbref.com/en/squads/11b6dba8/Lanus-Stats", "https://fbref.com/en/squads/9bf4eaf4/Newells-Old-Boys-Stats", "https://fbref.com/en/squads/a4570206/Defensa-y-Justicia-Stats", "https://fbref.com/en/squads/9aa97c75/Central-Cordoba-SdE-Stats", "https://fbref.com/en/squads/e2f19203/Instituto-Stats", "https://fbref.com/en/squads/7765008b/Belgrano-Stats", "https://fbref.com/en/squads/ac9a09b4/Godoy-Cruz-Stats", "https://fbref.com/en/squads/42a1ab8b/Atletico-Tucuman-Stats", "https://fbref.com/en/squads/950a95f2/Gimnasia-y-Esgrima-LP-Stats", "https://fbref.com/en/squads/e9ae80b7/Sarmiento-Stats", "https://fbref.com/en/squads/e5927bd8/Aldosivi-Stats", "https://fbref.com/en/squads/06c1606c/Banfield-Stats", "https://fbref.com/en/squads/5adc7e67/Union-Stats", "https://fbref.com/en/squads/41c139b6/Velez-Sarsfield-Stats", "https://fbref.com/en/squads/ceda2145/Talleres-Stats", "https://fbref.com/en/squads/d7a2603d/San-Martin-de-San-Juan-Stats"
    ],
    "MLS": [
        "https://fbref.com/en/squads/46024eeb/Philadelphia-Union-Stats", "https://fbref.com/en/squads/e9ea41b2/FC-Cincinnati-Stats", "https://fbref.com/en/squads/cb8b86a2/Inter-Miami-Stats", "https://fbref.com/en/squads/35f1b818/Nashville-SC-Stats", "https://fbref.com/en/squads/529ba333/Columbus-Crew-Stats", "https://fbref.com/en/squads/69a0fb10/New-York-Red-Bulls-Stats", "https://fbref.com/en/squads/46ef01d0/Orlando-City-Stats", "https://fbref.com/en/squads/eb57545a/Charlotte-FC-Stats", "https://fbref.com/en/squads/64e81410/New-York-City-FC-Stats", "https://fbref.com/en/squads/3c079def/New-England-Revolution-Stats", "https://fbref.com/en/squads/f9940243/Chicago-Fire-Stats", "https://fbref.com/en/squads/44117292/DC-United-Stats", "https://fbref.com/en/squads/1ebc1a5b/Atlanta-United-Stats", "https://fbref.com/en/squads/130f43fa/Toronto-FC-Stats", "https://fbref.com/en/squads/fc22273c/CF-Montreal-Stats", "https://fbref.com/en/squads/ab41cb90/Vancouver-Whitecaps-FC-Stats", "https://fbref.com/en/squads/91b092e1/San-Diego-FC-Stats", "https://fbref.com/en/squads/99ea75a6/Minnesota-United-Stats", "https://fbref.com/en/squads/6218ebd4/Seattle-Sounders-Stats", "https://fbref.com/en/squads/d076914e/Portland-Timbers-Stats", "https://fbref.com/en/squads/81d817a3/Los-Angeles-FC-Stats", "https://fbref.com/en/squads/ca460650/San-Jose-Earthquakes-Stats", "https://fbref.com/en/squads/415b4465/Colorado-Rapids-Stats", "https://fbref.com/en/squads/0d885416/Houston-Dynamo-Stats", "https://fbref.com/en/squads/b918956d/Austin-FC-Stats", "https://fbref.com/en/squads/15cf8f40/FC-Dallas-Stats", "https://fbref.com/en/squads/4acb0537/Sporting-Kansas-City-Stats", "https://fbref.com/en/squads/f7d86a43/Real-Salt-Lake-Stats", "https://fbref.com/en/squads/bd97ac1f/St-Louis-City-Stats", "https://fbref.com/en/squads/d8b46897/LA-Galaxy-Stats"
    ],
    "Brasileirão": [
        "https://fbref.com/en/squads/639950ae/Flamengo-Stats", "https://fbref.com/en/squads/03ff5eeb/Cruzeiro-Stats", "https://fbref.com/en/squads/f98930d1/Red-Bull-Bragantino-Stats", "https://fbref.com/en/squads/abdce579/Palmeiras-Stats", "https://fbref.com/en/squads/84d9701c/Fluminense-Stats", "https://fbref.com/en/squads/157b7fee/Bahia-Stats", "https://fbref.com/en/squads/289e8847/Mirassol-Stats", "https://fbref.com/en/squads/422bb734/Atletico-Mineiro-Stats", "https://fbref.com/en/squads/d9fdd9d9/Botafogo-RJ-Stats", "https://fbref.com/en/squads/2f335e17/Ceara-Stats", "https://fbref.com/en/squads/bf4acd28/Corinthians-Stats", "https://fbref.com/en/squads/d5ae3703/Gremio-Stats", "https://fbref.com/en/squads/6f7e1f03/Internacional-Stats", "https://fbref.com/en/squads/83f55dbe/Vasco-da-Gama-Stats", "https://fbref.com/en/squads/33f95fe0/Vitoria-Stats", "https://fbref.com/en/squads/a9d0ab0e/Fortaleza-Stats", "https://fbref.com/en/squads/712c528f/Santos-Stats", "https://fbref.com/en/squads/d081b697/Juventude-Stats", "https://fbref.com/en/squads/ece66b78/Sport-Recife-Stats"
    ],
    "Belgian Pro League": [
        "https://fbref.com/en/squads/1e972a99/Genk-Stats", "https://fbref.com/en/squads/f1e6c5f1/Club-Brugge-Stats", "https://fbref.com/en/squads/e14f61a5/Union-SG-Stats", "https://fbref.com/en/squads/08ad393c/Anderlecht-Stats", "https://fbref.com/en/squads/c2e6b53b/Antwerp-Stats", "https://fbref.com/en/squads/51e5a603/Gent-Stats", "https://fbref.com/en/squads/33c6b26e/Standard-Liege-Stats", "https://fbref.com/en/squads/09f00144/Mechelen-Stats", "https://fbref.com/en/squads/57b6cfb8/Westerlo-Stats", "https://fbref.com/en/squads/140e320a/Charleroi-Stats", "https://fbref.com/en/squads/27e981a3/OH-Leuven-Stats", "https://fbref.com/en/squads/868afa3f/Dender-Stats", "https://fbref.com/en/squads/e8d2adc4/Cercle-Brugge-Stats", "https://fbref.com/en/squads/80328a1e/Sint-Truiden-Stats", "https://fbref.com/en/squads/77193015/Kortrijk-Stats", "https://fbref.com/en/squads/c16e44ce/Beerschot-Wilrijk-Stats"
    ],
    "Eredivisie": [
        "https://fbref.com/en/squads/e334d850/PSV-Eindhoven-Stats", "https://fbref.com/en/squads/19c3f8c4/Ajax-Stats", "https://fbref.com/en/squads/fb4ca611/Feyenoord-Stats", "https://fbref.com/en/squads/2a428619/Utrecht-Stats", "https://fbref.com/en/squads/3986b791/AZ-Alkmaar-Stats", "https://fbref.com/en/squads/a1f721d3/Twente-Stats", "https://fbref.com/en/squads/e33d6108/Go-Ahead-Eagles-Stats", "https://fbref.com/en/squads/fc629994/NEC-Nijmegen-Stats", "https://fbref.com/en/squads/193ff7aa/Heerenveen-Stats", "https://fbref.com/en/squads/e3db180b/Zwolle-Stats", "https://fbref.com/en/squads/bd08295c/Fortuna-Sittard-Stats", "https://fbref.com/en/squads/146a68ce/Sparta-Rotterdam-Stats", "https://fbref.com/en/squads/bec05adb/Groningen-Stats", "https://fbref.com/en/squads/c882b88e/Heracles-Almelo-Stats", "https://fbref.com/en/squads/8ed04be8/NAC-Breda-Stats", "https://fbref.com/en/squads/f0479d7b/Willem-II-Stats", "https://fbref.com/en/squads/bb14adb3/RKC-Waalwijk-Stats", "https://fbref.com/en/squads/2b41acb5/Almere-City-Stats"
    ]
}

# --- CONFIGURACIÓN PARA EXPORTAR ---
output_dir = './data'
output_filename = 'passing_outside_top5.csv'
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
            # Targeting the 6th table which is 'Shooting'
            df = df_list[5]

            squad_name_match = re.search(r'/squads/[^/]+/([^-]+(?:-[^-]+)*)-Stats', url)
            if squad_name_match:
                squad_name = squad_name_match.group(1).replace("-", " ")
            else:
                squad_name = "Unknown Squad"

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(0)
            
            # --- NUEVA COLUMNA DE LIGA ---
            df['League'] = league
            df['Squad'] = squad_name

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
        time.sleep(5)

if dfs:
    passing_df = pd.concat(dfs, ignore_index=True)
    df_cleaned = passing_df[~passing_df['Player'].str.contains('Player|Squad Total', na=False)]
    
    # --- REORDENAR COLUMNAS (OPCIONAL PERO RECOMENDADO) ---
    # Colocar 'League' y 'Squad' al principio para mayor claridad.
    cols_order = ['League', 'Squad', 'Player'] + [col for col in df_cleaned.columns if col not in ['League', 'Squad', 'Player']]
    df_cleaned = df_cleaned[cols_order]

    # --- NUEVA CONDICIÓN PARA RENOMBRAR COLUMNAS 'Prog' DUPLICADAS ---
    # Este bloque renombra las columnas 'Prog' para evitar duplicados, añadiendo un sufijo numérico.
    # Requiere Python 3.8 o superior por el uso del operador Walrus (:=).
    cols, count = [], 1
    for column in df_cleaned.columns:
        if column == 'Prog':
            cols.append(f'Prog_{count}')
            count += 1
        else:
            cols.append(column)
    df_cleaned.columns = cols
    
    df_cleaned.to_csv(
        output_path,
        index=False
    )
    print(f"\n¡Proceso completado! Archivo guardado en: {output_path}")
else:
    print("\nNo se pudo procesar ningún dato.")
