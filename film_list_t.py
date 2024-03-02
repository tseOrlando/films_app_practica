
from typing import List
import json

from film_t import film_t
from persistence_film_t import persistence_film_t

class film_list_t():

    def __init__ (self, persistence_film : persistence_film_t):
        self._films = []
        self._last_id = 0
        self._persistence_film :persistence_film_t = persistence_film
        

    @property
    def films(self) -> List[film_t]: return self._films
    
    @property
    def last_id(self) -> int: return self._last_id

    @property
    def persistence_film(self) -> persistence_film_t: return self._persistence_film
    
    def __repr__(self): return self.to_json()
    

    def to_json(self):
        
        films = []

        for film in self._films:
            films.append(json.loads(film.to_json()))
    
        return json.dumps({"pelicules": films})

    def read_like(self, opt : int, id : int):

        if opt == 0:
            self._films = self._persistence_film.read()
            return self._films
        
        elif opt == 1: 

            self._last_id = id

            pack = self._persistence_film.get_films_by_10(self._last_id)

            self._films = pack["films"]
            self._last_id = pack["last_id"]

            return {"last_id" : self._last_id , "films" : self.films}
        
        else: return []

    def modify_like(self, opt : int, film_data):

        if opt == 0:
            self.persistence_film.save(film_t(film_data[0], film_data[1], film_data[2], film_data[3], persistencia=self._persistence_film))
        elif opt == 1:
            self.persistence_film.change(film_data)




