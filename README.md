# Movie Recommendation API

## Descripción
Este proyecto es una API desarrollada con FastAPI que permite realizar diversas operaciones relacionadas con un conjunto de datos de películas. Entre las principales funcionalidades se incluyen:

- Obtener información de actores y directores.
- Consultar las películas más populares.
- Visualizar las películas mejor puntuadas por año.
- Sistema de recomendación basado en similitud del coseno.
- Obtener detalles específicos de una película.

## Requisitos

- Python 3.8+
- FastAPI
- SQLite
- Pandas
- Scikit-learn
- Matplotlib (para visualización opcional)

Instalar dependencias:
```bash
pip install fastapi uvicorn pandas scikit-learn matplotlib
```

## Estructura del proyecto
```
M-Pindividual/
├── API/
│    ├── app/
│         ├── __init__.py
│         └── main.py
│   ├── Scripts/
│         └── convert_csv_to_sqlite.py
├── data/
│   └── database.db
│    ├── requirements.txt
│    ├── transformacion.py
└── README.md
```

- **main.py**: Archivo principal con la lógica de la API.
- **transformaciones.py**: Archivo auxiliar para funciones de transformación.
- **database.db**: Base de datos SQLite con los datos de las películas.
- **convert_csv_to_sqlite.py**: Conversor de archivos csv a SQLite.
- **requirements.txt**: Los requerimientos necesarios para que funcione.

## Endpoints

### 1. Obtener Actores
**Endpoint:** `/actors/`

Retorna una lista de actores presentes en la base de datos.

**Ejemplo de uso:**
```bash
GET /actors/
```
**Respuesta:**
```json
[
    "Actor 1",
    "Actor 2",
    "Actor 3"
]
```

### 2. Obtener Directores
**Endpoint:** `/directors/`

Retorna una lista de directores presentes en la base de datos.

**Ejemplo de uso:**
```bash
GET /directors/
```
**Respuesta:**
```json
[
    "Director 1",
    "Director 2",
    "Director 3"
]
```

### 3. Películas Más Populares
**Endpoint:** `/movies/popular/`

Retorna las 10 películas más populares.

**Ejemplo de uso:**
```bash
GET /movies/popular/
```
**Respuesta:**
```json
[
    {
        "title": "Movie 1",
        "popularity": 99.5
    },
    {
        "title": "Movie 2",
        "popularity": 95.3
    }
]
```

### 4. Películas Mejor Puntuadas por Año
**Endpoint:** `/movies/top/{year}/`

Retorna las 5 películas mejor puntuadas para un año específico.

**Ejemplo de uso:**
```bash
GET /movies/top/2021/
```
**Respuesta:**
```json
[
    {
        "title": "Movie 1",
        "vote_average": 8.7
    },
    {
        "title": "Movie 2",
        "vote_average": 8.5
    }
]
```

### 5. Sistema de Recomendación
**Endpoint:** `/recommendations/{title}/`

Dado el título de una película, retorna 5 películas recomendadas basadas en similitud del coseno.

**Ejemplo de uso:**
```bash
GET /recommendations/Inception/
```
**Respuesta:**
```json
[
    "Movie 1",
    "Movie 2",
    "Movie 3",
    "Movie 4",
    "Movie 5"
]
```

### 6. Obtener Detalles de una Película
**Endpoint:** `/movie/{title}/`

Retorna los detalles de una película específica por título.

**Ejemplo de uso:**
```bash
GET /movie/Inception/
```
**Respuesta:**
```json
{
    "title": "Inception",
    "release_date": "2010-07-16",
    "budget": 160000000,
    "revenue": 825532764,
    "vote_average": 8.3
}
```

## Ejecución

Para ejecutar la aplicación:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Notas
- Asegúrese de tener la base de datos `database.db` en la ruta especificada.
- Puede personalizar las rutas o lógica en `main.py` según sea necesario.

## Autor
- Pedro

---
