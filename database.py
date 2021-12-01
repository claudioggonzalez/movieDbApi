#!/bin/python3

import sqlite3

class Database:
	def __init__(self, dbname):
		if __name__ == "__main__":
			#print("Openening database:",dbname)
			self.connection = sqlite3.connect("./" + dbname)
		else:
			#print("Openening database:",dbname)
			self.connection = sqlite3.connect("./" + dbname, check_same_thread=False)

		self.cursor = self.connection.cursor()

	def getAllMovies(self):
		self.cursor.execute("SELECT * FROM movieData")
		return self.cursor.fetchall()

	def getMovieById(self, id: int):
		self.cursor.execute(f"SELECT * FROM movieData WHERE id = {id}")
		return self.cursor.fetchall()

	def getMovieByTitle(self, title: str):
		self.cursor.execute(f"SELECT * FROM movieData WHERE title LIKE '%{title}%' OR alTtitle LIKE '%{title}%'")
		return self.cursor.fetchall()

	def getMovieBatch(self, batchSize: int, limitDate: str):
		self.cursor.execute(f"SELECT * FROM movieData WHERE status = 1 AND subtitle = true AND year >= 2020 AND downloadDate >= date('{limitDate}') ORDER BY downloadDate ASC LIMIT {batchSize}")
		return self.cursor.fetchall()

	def addMovie(self, title: str, altTitle:str=None, year:int=None, originCountry:str=None, releaseDate:str=None, downloadDate:str=None, subtitle:bool=False,status:int=0):
		queryData = [title, altTitle, year, originCountry, releaseDate, downloadDate, subtitle, status]
		self.cursor.execute("INSERT INTO movieData VALUES(null,?,?,?,?,?,?,?,?)", queryData)
		self.connection.commit()

	def updateMovieById(self, id: int, data: list):
		self.cursor.execute(f"UPDATE movieData SET title='{data[0]}', altTitle='{data[1]}', year={data[2]}, originCountry='{data[3]}', releaseDate='{data[4]}', downloadDate='{data[5]}', subtitle={data[6]}, status={data[7]} WHERE id = {id}")
		self.connection.commit()

	def deleteMovieById(self, id: int):
		self.cursor.execute(f"DELETE FROM movieData WHERE id = {id}")
		self.connection.commit()


if __name__ == "__main__":
	Database()

"""Sentencias de Creacion de Tablas"""
"""self.cursor.execute()"""
"""self.cursor.execute()"""
