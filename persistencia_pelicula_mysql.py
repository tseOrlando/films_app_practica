#!/bin/usr/python3

from ipersistencia_pelicula import IPersistencia_pelicula
from pelicula import Pelicula
from typing  import List
import mysql.connector
import logging

class Persistencia_pelicula_mysql(IPersistencia_pelicula):
    def __init__(self, credencials) -> None:
        self._credencials = credencials
        self._conn = mysql.connector.connect(
                host=credencials["host"],
                user=credencials["user"],
                password=credencials["password"],
                database=credencials["database"]
                )
        if not self.check_table():
            self.create_table()

    def check_table(self):
        try:
            cursor = self._conn.cursor(buffered=True)
            cursor.execute("SELECT * FROM PELICULA;")
            cursor.reset()
        except mysql.connector.errors.ProgrammingError:
            return False
        return True
    
    def count(self) -> int:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        count = cursor.rowcount
        return count
    
    def totes(self) -> List[Pelicula]:
        cursor = self._conn.cursor(buffered=True)
        query = "select id, titulo, anyo, puntuacion, votos from PELICULA;"
        cursor.execute(query)
        registres = cursor.fetchall()
        cursor.reset()
        resultat = []
        for registre in registres:
            pelicula = Pelicula(registre[1],registre[2],registre[3],registre[4],self,registre[0])
            resultat.append(pelicula)
        return resultat
    
    def totes_pag(self, id=None) -> List[Pelicula]:
        return List[Pelicula(x) for x in self._conn.cursor().execute(f"SELECT * FROM PELICULA WHERE ID > {id} LIMIT 10")]
    
    def desa(self,pelicula:Pelicula):
        cur = self._conn.cursor()
        cur.execute(f"INSERT INTO PELICULA(TITULO, ANYO, PUNTUACION, VOTOS) VALUES ({pelicula.titol}, {pelicula.any}, {pelicula.puntuacio}, {pelicula.vots});")
        self._conn.commit()
    
    def llegeix(self, any: int) -> list:
        return [peli for peli in self._conn.cursor().execute(f"SELECT ANYO FROM PELICULA WHERE ANYO = {any}")]
        
    def canvia(self, params:dict, pelicula:Pelicula):
        active_params = {"TITULO": False, "ANYO": False, "PUNTUACION": False, "VOTOS": False}
        cur = self._conn.cursor()
        peli_args = {}

        if any(pgiven > 4 or pgiven <= -1 for pgiven in params.values()):
            return 
        
        for pgiven in params:
            for param in active_params:
                active_params[param] = True
                peli_args.update({active_params[param]:pelicula.__dict__[param]})
        
        for arg, value in peli_args.items():
            cur.execute(f"UPDATE PELICULA SET {arg} = {value} WHERE id = {pelicula.id};")
            self._conn.commit()