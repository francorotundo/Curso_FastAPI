from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()
app.title = "My first app in FastAPI"
app.version = "0.0.1"

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
def create_movie(
    id: int = Body(), 
    title: str = Body(), 
    overview: str = Body(), 
    year: int = Body(), 
    rating: float = Body(), 
    category: str= Body()
    ):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })
    return movies


@app.put('/movies/{id}', tags=['movies'])
def update_movie(
    id: int, 
    title: str = Body(), 
    overview: str = Body(), 
    year: int = Body(), 
    rating: float = Body(), 
    category: str= Body()
    ):
    for item in movies:
        if item['id'] == id:
            item['title'] = title
            item['overview'] = overview
            item['rating'] = rating
            item['year'] = year
            item['category'] = category
            return JSONResponse(content=movies)


@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id = int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content=movies)
