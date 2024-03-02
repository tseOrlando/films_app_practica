
from film_t import film_t

from abc import ABC, abstractclassmethod
from typing import List

class persistence_film_t(ABC):
    
    @abstractclassmethod
    def get_films(self):
        pass

    @abstractclassmethod
    def get_films_by_10(self, id: int):
        pass
    
    @abstractclassmethod
    def save(self, film: film_t):
        pass

    @abstractclassmethod
    def change(self, params :dict):
        pass

    @abstractclassmethod
    def read(self, year: int):
        pass