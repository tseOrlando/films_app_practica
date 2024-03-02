
from persistence_film_t import persistence_film_t
from film_t import film_t

import mysql.connector, os
from typing import List

class persistence_film_mysql_t(persistence_film_t):
    
    def __init__(self, credentials) -> None:

        self.credentials = credentials
        self.peer = mysql.connector.connect(host=credentials["host"], user=credentials["user"], password=credentials["password"], database=credentials["database"])
    
    def count(self) -> int:

        cursor = self.peer.cursor()

        cursor.execute("SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS FROM PELICULA;")

        return cursor.rowcount
    
    def get_films(self) -> List[film_t]:

        cursor = self.peer.cursor()
        
        cursor.execute("SELECT ID, TITULO, ANYO, PUNTUACION, VOTOS FROM PELICULA;")

        return [film_t(reg[1], reg[2], reg[3], reg[4], self, reg[0]) for reg in cursor.fetchall()]
    
    
    def get_films_by_10(self, id = None) -> List[film_t]:

        cursor = self.peer.cursor()
        
        cursor.execute(f"SELECT * FROM PELICULA WHERE ID > {id} LIMIT 10")

        films = [film_t(reg[1], reg[2], reg[3], reg[4], self, reg[0]) for reg in cursor.fetchall()]

        last_id = max([film.id for film in films])

        return {"last_id" : last_id, "films" : films}
    
    def save(self, film :film_t) -> None:
        
        cursor = self.peer.cursor()

        #me dirás tú porque mierda falla esta putísima puta mierda de sentencia sql
        cursor.execute(f"INSERT INTO PELICULA (TITULO, ANYO, PUNTUACION, VOTOS) VALUES ( '{film.titol}', {film.any}, {film.puntuacio}, {film.vots} );")
        
        self.peer.commit()

        cursor.close()

        print("\n pel.licula emmagatzemada\n")
    
    def read(self):

        os.system("clear") #ekk

        year = input("Proporciona un any per buscar-hi pelicules\n")

        cursor = self.peer.cursor()
        cursor.execute(f"SELECT * FROM PELICULA WHERE ANYO = {year}")

        return cursor.fetchall()
        
    def change(self, params :dict):

        os.system("clear") #ekk

        active_params = {"1" : {"TITULO": False}, "2" : {"ANYO": False},  "3" : {"PUNTUACION": False}, "4" : {"VOTOS": False}}
        
        cursor = self.peer.cursor()
        
        for pg in params:
            for index in active_params:
                for ap in active_params[index]:
                    if pg == index:
                        active_params[index][ap] = True
                        
        print(f"\nValors a modificar : ({[param_name.lower() for index in active_params for param_name, value in active_params[index].items() if value]})\n")

        film_id = input("Introdueix la ID de la pel.licula que vols canviar\n")
        
        os.system("clear") #ekk

        for index, active_param in active_params.items():
            for param, active in active_param.items():
                if active:
                    value = input(f"Escriu el valor nou a donar a {param.lower()}\n")
                    cursor.execute(f"UPDATE PELICULA SET {param} = '{value}' WHERE ID = {film_id};")
                    self.peer.commit()

                    os.system("clear") #ekk