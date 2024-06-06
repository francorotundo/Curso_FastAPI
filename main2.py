from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
app.title = "My first app in FastAPI"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None #Cuando el valor del la variable es opcional, tambien se puede utilizar para este caso --> int | None = None
    title: str = Field(min_length=5, max_length=15)#con Field se le valida cuando tenga menos de 15 caracteres, tambien se le puede sumar la caracteristica default="algo"
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)#con la abreviatura "le" se especifica que el numero sea menor a 2022
    rating: float = Field(ge=1, le=10) #ge: mayor o igual que, le: menor o igual que
    category: str = Field(min_lenght = 5, max_lengh = 15)
    
    class Config:
        #Permite colocar los valors por defecto que apareceran en cada input
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripción de la Pelicula",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }


movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar 2",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },{
        "id": 3,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Romantic"
    }
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse("<h1>Hello Franco</h1>")

@app.get('/movies', tags= ['movies'])
def get_movies():
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags= ['movies'])
def get_movie(id: int = Path(ge=1, le= 2000)):
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item['title'])
    return JSONResponse(content=[])
    
@app.get('/movies/', tags= ['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    data = [ item for item in movies if item['category'] == category]
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content=movies)

@app.put('/movies/{id}', tags=['movies'])
def update_movie(
    id: int, 
    movie: Movie
    ):
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['rating'] = movie.rating
            item['year'] = movie.year
            item['category'] = movie.category
            return JSONResponse(content=movies)
    

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id = int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content=movies)