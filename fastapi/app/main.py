from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
from contextlib import closing
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



app = FastAPI()

DATABASE_PATH = "C:/Users/Pedro/Desktop/M-Pindividual/data/database.db"

# Mapeo de meses
MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}

# Mapeo de días
DIAS = {
    "lunes": 0,
    "martes": 1,
    "miércoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sábado": 5,
    "domingo": 6
}

# Función para realizar consultas a la base de datos
def query_db(query, params=()):
    try:
        with closing(sqlite3.connect(DATABASE_PATH)) as conn:
            df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar la consulta: {e}")





# Endpoint: Cantidad de filmaciones por día de la semana
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    dia = dia.lower()
    if dia not in DIAS:
        raise HTTPException(status_code=400, detail="Día inválido. Use un día en español (ej: lunes, martes).")

    dia_numero = DIAS[dia]
    query = """
    SELECT COUNT(*) AS cantidad
    FROM movies
    WHERE strftime('%w', release_date) = ?
    """
    df = query_db(query, (str(dia_numero),))
    cantidad = int(df.iloc[0]["cantidad"])

    return {
        "dia": dia.capitalize(),
        "cantidad": cantidad,
        "mensaje": f"{cantidad} películas fueron estrenadas en los días {dia.capitalize()}."
    }




# Endpoint: Cantidad de filmaciones por mes
@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    mes = mes.lower()
    if mes not in MESES:
        raise HTTPException(status_code=400, detail="Mes inválido. Use un mes en español (ej: enero, febrero).")

    mes_numero = MESES[mes]
    query = """
    SELECT COUNT(*) AS cantidad
    FROM movies
    WHERE strftime('%m', release_date) = ?
    """
    df = query_db(query, (f"{mes_numero:02}",))
    cantidad = int(df.iloc[0]["cantidad"])

    return {
        "mes": mes.capitalize(),
        "cantidad": cantidad,
        "mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}."
    }



# Endpoint: Información sobre el score de un título
@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):
    query = """
    SELECT title, Anio AS release_year, popularity AS score
    FROM movies
    WHERE LOWER(title) = LOWER(?)
    LIMIT 1
    """
    df = query_db(query, (titulo,))

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró una película con el título '{titulo}'.")

    titulo = df.iloc[0]["title"]
    anio_estreno = df.iloc[0]["release_year"]
    score = df.iloc[0]["score"]

    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {anio_estreno} con un score/popularidad de {score}."
    }



# Endpoint: Información sobre los votos de un título
@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo: str):
    query = """
    SELECT title, Anio AS release_year, vote_count, vote_average
    FROM movies
    WHERE LOWER(title) = LOWER(?)
    LIMIT 1
    """
    df = query_db(query, (titulo,))

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró una película con el título '{titulo}'.")

    titulo = df.iloc[0]["title"]
    anio_estreno = df.iloc[0]["release_year"]
    votos = df.iloc[0]["vote_count"]
    promedio = df.iloc[0]["vote_average"]

    if votos < 2000:
        return {
            "mensaje": f"La película '{titulo}' fue estrenada en el año {anio_estreno}, pero no cumple la condición de tener al menos 2000 votos."
        }

    return {
        "mensaje": f"La película '{titulo}' fue estrenada en el año {anio_estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}."
    }




# Endpoint: Información sobre un actor
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    try:
        # Consulta para obtener las películas y el retorno asociados al actor
        query = """
        SELECT m.title, m."return"
        FROM characters c
        JOIN movies m ON c.id_movies = m.id
        WHERE c.name = ?
        """
        df = query_db(query, (nombre_actor,))

        # Verificar si el DataFrame está vacío
        if df.empty:
            return {"mensaje": f"No se encontraron películas para el actor {nombre_actor}."}

        # Calcular las métricas
        total_retorno = df["return"].sum()
        cantidad_peliculas = len(df)
        promedio_retorno = total_retorno / cantidad_peliculas if cantidad_peliculas > 0 else 0

        # Resultado
        return {
            "actor": nombre_actor,
            "cantidad_peliculas": cantidad_peliculas,
            "total_retorno": total_retorno,
            "promedio_retorno": promedio_retorno
        }
    except ZeroDivisionError:
        return {"error": "El actor no tiene suficientes datos para calcular el promedio."}
    except sqlite3.Error as e:
        return {"error": f"Error en la base de datos: {str(e)}"}
    except ValueError as e:
        return {"error": f"Error en los datos recuperados: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}




# Endpoint: Información sobre un director
@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    query = """
    SELECT m.title, m.release_date, m.budget, m.revenue, m."return"
    FROM directors d
    JOIN movies m ON d.id_movies = m.id
    WHERE d.name = ?
    """
    df = query_db(query, (nombre_director,))

    if df.empty:
        return {"mensaje": f"No se encontraron películas para el director {nombre_director}."}

    df["ganancia"] = df["revenue"] - df["budget"]
    total_retorno = df["return"].sum()

    peliculas = df[["title", "release_date", "return", "budget", "ganancia"]].to_dict(orient="records")

    return {
        "director": nombre_director,
        "total_retorno": total_retorno,
        "peliculas": peliculas
    }





    
def load_data() -> pd.DataFrame:
    """Carga y procesa los datos desde SQLite."""
    try:
        query = """
        SELECT title, tagline, original_language, vote_average, popularity, release_date
        FROM movies
        WHERE title IS NOT NULL AND vote_average > 0
        """
        df = query_db(query)
    except HTTPException as e:
        raise e

    # Rellenar valores nulos
    df['tagline'] = df['tagline'].fillna('')
    
    # Crear columna de características combinadas
    df['features'] = (
        df['title'] + " " +
        df['tagline'] + " " +
        df['original_language']
    )
    return df

# Cargar y procesar los datos una sola vez
movies_df = load_data()

# Vectorizar la columna 'features'
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies_df['features'])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear un índice para acceder a las películas por título
indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()

# Endpoint para obtener recomendaciones
@app.get("/recommendations/", response_model=List[Dict[str, str]])
def get_recommendations(title: str, top_n: int = 5) -> List[Dict[str, str]]:
    # Verificar si el título existe en el DataFrame
    if title not in indices:
        raise HTTPException(status_code=404, detail=f"La película '{title}' no se encuentra en la base de datos.")
    
    # Obtener el índice de la película ingresada
    idx = indices[title]
    
    # Obtener las puntuaciones de similitud de esa película con todas las demás
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordenar las películas por similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Seleccionar las N películas más similares (excluyendo la misma película)
    sim_scores = sim_scores[1:top_n + 1]
    
    # Obtener los índices de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]
    
    # Construir las recomendaciones
    recommendations = movies_df.iloc[movie_indices][['title', 'tagline', 'vote_average', 'popularity', 'release_date']]
    
    # Convertir release_date, vote_average y popularity a cadena
    recommendations['release_date'] = recommendations['release_date'].astype(str)
    recommendations['vote_average'] = recommendations['vote_average'].astype(str)
    recommendations['popularity'] = recommendations['popularity'].astype(str)

    # Convertir el resultado en una lista de diccionarios
    return recommendations.to_dict(orient='records')

# Ruta de prueba
@app.get("/")
def root():
    return {"message": "Bienvenido al sistema de recomendación de películas. Usa /recommendations/?title=<TITULO> para obtener recomendaciones."}