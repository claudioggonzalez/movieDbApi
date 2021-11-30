#!/bin/python3

from pydantic import BaseModel, Field
from fastapi import FastAPI, status, HTTPException, Header
from typing import Optional
import configparser

from database import Database

print("Iniciando...")
try:
	config = configparser.ConfigParser()
	config.read('movieDbApi.conf')

	DATABASE_NAME = config['Database']['DBNAME']
	START_DATE = config['Date']['STARTDATE']
	BATCH_SIZE = config['General']['BATCHSIZE']

	db = Database(DATABASE_NAME)
except:
	print("ERROR Iniciando Aplicacion...!!!")
	exit(1)

app = FastAPI()
#app = FastAPI(dependencies=[Depends(verify_key)])

API_VERSION = 0.1

class Movie(BaseModel):
	title: str= Field (...,description="Título original")
	altTitle: Optional[str] = Field (None, description="Título alternativo.")
	year: int = Field (..., ge=1900, lt=2100, description="Año de publicación (YYYY).")
	originCountry: Optional[str] = Field (None, description="Pais de origen.")
	releaseDate: Optional[str] = Field (None, description="Fecha de lanzamiento (YYYY-MM-DD).")
	downloadDate: Optional[str] = Field (None, description="Fecha de descarga (YYYY-MM-DD).")
	subtitle: Optional[bool] = Field(False, description="Existencia de subtitulos (true/false).")
	status: int = Field (0, ge=0, lt=4, description="Estado (0:Registrada, 1:Descargada, 2:Pendiente, 3:Vista)")

def convertToJson(mode, idx, name=None):
	listData = []

	if mode == "id":
		query = db.getMovieById(idx)
	elif mode == "title":
		query = db.getMovieByTitle(name)
	elif mode == "batch":
		query = db.getMovieBatch(BATCH_SIZE,START_DATE)
	else:
		query = db.getAllMovies()

	for data in query:
		listData.append({"id": data[0],
						"title": data[1],
						"altTile": data[2],
						"year": data[3],
						"originCountry": data[4],
						"releaseDate": data[5],
						"downloadDate": data[6],
						"subtitle": data[7],
						"status": data[8]})
	return listData

#@app.get("/api/", dependencies=[Depends(verify_key)])
@app.get(path="/api/")
def getMovies():
	return {"name": "MovieDBAPI", "description": "API para control de películas", "version": API_VERSION}

@app.get(path="/api/getAll")
def getMovies():
	resp = convertToJson("all",0,None)
	if len(resp) > 0:
		return convertToJson("all",0,None)
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")

@app.get(path="/api/getId/{id:int}/")
def getMovieId(id):
	resp = convertToJson("id",id,None)
	if len(resp) > 0:
		return resp
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")

@app.get(path="/api/getTitle/{title:str}/")
def getMovieTitle(title):
	resp = convertToJson("title",0,title)
	if len(resp) > 0:
		return resp
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")

@app.get(path="/api/getBatch/")
def getMovieBatch():
	resp = convertToJson("batch",0,None)
	if len(resp) > 0:
		return resp
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movies not found")

@app.post(path="/api/addMovie/", status_code=status.HTTP_201_CREATED)
def addMovie(movie: Movie):
	db.addMovie(movie.title, movie.altTitle, movie.year, movie.originCountry, movie.releaseDate, movie.downloadDate, movie.subtitle, movie.status)
	resp = convertToJson("title",0,movie.title)
	if len(resp) > 0:
		return resp
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie could not be added")

@app.put(path="/api/updateMovie/{id:int}/", status_code=status.HTTP_202_ACCEPTED)
def updateMovieData(id, movie: Movie):
	db.updateMovieById(id, [movie.title, movie.altTitle, movie.year, movie.originCountry, movie.releaseDate, movie.downloadDate, movie.subtitle, movie.status])
	resp = convertToJson("id",id,None)
	if len(resp) > 0:
		return resp
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie could not be updated")

@app.delete(path="/api/deleteMovie/{id:int}/", status_code=status.HTTP_202_ACCEPTED)
def deleteMovie(id):
	db.deleteMovieById(id)
	resp = convertToJson("id",id,None)
	if len(resp) == 0:
		return {"id":id,"status":"Deleted"}
	else:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie could not be deleted")
