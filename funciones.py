import pandas as pd
import fastapi
from fastapi import FastAPI
import pyarrow.parquet as pq
import pickle

# Cargar los DataFrames desde los archivos parquet
games=pd.read_parquet("games.parquet")
#items=pd.read_parquet("items.parquet")
reviews=pd.read_parquet("reviews.parquet")
new_df = pd.read_parquet('modelo.parquet')

#modelo.pkl para la función 6
with open ('modelo.pkl', 'rb') as archivo:
    modelo = pickle.load(archivo)

#funcion 1
def developer(desarrollador):
    if desarrollador not in games['developer'].unique():
        return {'error': 'El Desarrollador especificado no existe.'}
    #llamo a las columnas que necesito
    df = games[["item_id", "price","developer","año_lanzamiento"]] 
    
    #llamo al desarrollador
    developer = df[df["developer"] == desarrollador]
    
    #obtengo la cantidad por año 
    cantidad_item = developer.groupby("año_lanzamiento")["item_id"].count() 
    
    #juegos gratuitos del desarrollador
    gratis = developer[developer["price"] == 0] 
    
    #cantidad juegos gratis por año 
    total_gratis= gratis.groupby("año_lanzamiento")["price"].count() 

    #porcentaje gratis por año 
    cont_gratis_año = round((total_gratis/cantidad_item)*100,2) 

    #asigno nombre a las series
    cantidad_item.name = "Cantidad de Items"

    cont_gratis_año.name = "Contenido Free"
    #unimos las dos tablas para hacerla unica
    tabla = pd.merge(cantidad_item, cont_gratis_año,on="año_lanzamiento").reset_index() 

    #reemplazo los nan por 0
    tabla = tabla.fillna(0) 
    
    tabla["Contenido Free"] = tabla["Contenido Free"].apply(lambda x: f"{x}%")
    #convierto la tabla en diccionario
    diccionario = tabla.to_dict(orient="records") 
    
    return diccionario


#funcion 2 
#Realizar la unión de los DataFrames
merged_reviews_games = reviews.merge(games[['item_id', 'price']])
merged_reviews_games.drop(columns=['helpful','año',"sentiment_analysis"], inplace=True)

def userdata(user_id):
    if user_id not in merged_reviews_games['user_id'].unique():
        return {'error': 'El usuario especificado no existe.'}
    # Filtrar los datos para el usuario especificado
    user_data = merged_reviews_games[merged_reviews_games['user_id'] == user_id]
    # Calcular la cantidad de dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()

    # Calcular el porcentaje de recomendación en base a reviews.recommend
    recomendacion = user_data['recommend'].sum()
    porcentaje_recomendacion = recomendacion / len(user_data) * 100

    # Calcular la cantidad de items
    cantidad_de_items = user_data['item_id'].nunique()

    # Crear un diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': dinero_gastado,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }

    return resultados

'''
#funcion 3
merged_items_games=pd.merge(games,items,on="item_id")

def UserForGenre(genero):
    if not genero in merged_items_games.columns:
        return f"El género {genero} no existe en la base de datos."

    df_genero = merged_items_games[merged_items_games[genero] == 1]

    usur_mas_horas = df_genero.groupby("user_id")["playtime_forever"].sum().idxmax()

    filtro_usuario = df_genero[df_genero["user_id"] == usur_mas_horas]

    horas_jugadas_año = filtro_usuario.groupby("año_lanzamiento")["playtime_forever"].sum()

    registro = horas_jugadas_año.to_dict()

    Horas_por_año = {}
    for clave, valor in registro.items():
        clave_formateada = f'Año: {int(clave)}'
        valor_formateado = int(valor)
        Horas_por_año[clave_formateada] = valor_formateado

    return {"Usuario con más horas jugadas": usur_mas_horas, "Horas jugadas por año": Horas_por_año}
'''



#funcion 4

def best_developer_year(año: int):
    # Realizar la unión de los DataFrames
    merged_df = pd.merge(reviews, games, on='item_id')
    if año not in merged_df['año'].unique():
        return {'error': 'El año especificado no existe.'}

    # Filtrar los juegos por año y por recomendación positiva
    df_year = merged_df[(merged_df['año'] == año) & (merged_df['recommend'] == True) & (merged_df['sentiment_analysis'] == 2)]

    # Contar el número de juegos recomendados por desarrollador y devolver los tres primeros desarrolladores
    top_desarrolladores = df_year['developer'].value_counts().head(3).index.tolist()

     # Devolver el top 3 de desarrolladores
    return {"Puesto 1" : top_desarrolladores[0], "Puesto 2" : top_desarrolladores[1], "Puesto 3" : top_desarrolladores[2]}
    

#funcion 5
merged = reviews.merge(games[['item_id', 'price',"developer"]], on='item_id')
def developer_reviews_analysis(desarrolladora:str):
    if desarrolladora not in games['developer'].unique():
        return {'error': 'El Desarrollador especificado no existe.'}
    
    #filtrar las columnas a utilizar 
    df = merged[['user_id', 'item_id','developer','año','sentiment_analysis']] 
    #filtrar los datos por desarrolladora
    df_merged = df[df["developer"] == desarrolladora] 

    # Se obtienen la cantidad de reviews positivas y negativas
    reviews_positivas = df_merged[df_merged["sentiment_analysis"] == 2].shape[0] 
    reviews_negativas = df_merged[df_merged["sentiment_analysis"] == 0].shape[0]

    # Se crea un string con el resumen de las reviews
    resumen_reviews = f"[Negative = {reviews_negativas}, Positive = {reviews_positivas}]" 
    # Se crea un diccionario con los resultados obtenidos
    dicc = {desarrolladora : resumen_reviews} 

    # Se devuelve un diccionario con los resultados obtenidos
    return dicc
 

#funcion 6
def recomendacion_usuario( id_usuario ):
    lista=[]
    if id_usuario not in new_df['user_id'].unique():
        return {'error': 'El usuario especificado no existe.'}
    
    #Crear una lista de juegos valorados por el usuario
    juegos_valorados = new_df[new_df['user_id'] == id_usuario]['app_name'].unique()

    #Crear una lista de todos los juegos disponibles
    todos_los_juegos = new_df['app_name'].unique()

    #Crear una lista de juegos no valorados por el usuario específico
    juegos_no_valorados = list(set(todos_los_juegos) - set(juegos_valorados))

    #Generar predicciones para los juegos no valorados por el usuario
    predicciones = [modelo.predict(id_usuario, juego) for juego in juegos_no_valorados]

    #Ordenar las predicciones en base a la valoración y obtener los juegos recomendados
    recomendaciones = sorted(predicciones, key=lambda x: x.est, reverse=True)[:5]  # Obtener las 5 mejores recomendaciones

  # Almacenar los nombres de los juegos recomendados en una lista
    juegos_recomendados = [recomendacion.iid for recomendacion in recomendaciones]
    
    # Crear un diccionario con los nombres de los juegos recomendados
    recomendaciones_dict = {
        'Juego 1': juegos_recomendados[0],
        'Juego 2': juegos_recomendados[1],
        'Juego 3': juegos_recomendados[2],
        'Juego 4': juegos_recomendados[3],
        'Juego 5': juegos_recomendados[4]
    }
    
    # Devolver el diccionario con los nombres de los juegos recomendados
    return recomendaciones_dict
    