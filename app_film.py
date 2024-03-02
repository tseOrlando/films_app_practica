#!/usr/bin/python3

import os, yaml, json
from film_t import film_t

from persistence_film_mysql_t import persistence_film_mysql_t
from film_list_t import film_list_t

path_configuration_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configuracio.yml') 
last_id_handler = 0

def cls():
    os.system('clear')

def display_result(result : list) -> None:
    for info in result:
        print(info)

def get_configuration(path_configuration_file):

    config = {}
    
    with open(path_configuration_file, 'r') as conf:
        config = yaml.safe_load(conf)

    return config

def get_persistences(configuration : dict):

    credentials = {}

    if configuration["base de dades"]["motor"].lower().strip() == "mysql":

        credentials['host']     = configuration["base de dades"]["host"]
        credentials['user']     = configuration["base de dades"]["user"]
        credentials['password'] = configuration["base de dades"]["password"]
        credentials['database'] = configuration["base de dades"]["database"]

        return {'pelicula': persistence_film_mysql_t(credentials)}
    
    else: return {'pelicula': None}

def show_list(film_list :film_list_t):

    cls()
    print(json.dumps(json.loads(film_list.to_json()), indent=4), v=0.01)

def get_film_list():
    return film_list_t(get_persistences(get_configuration(path_configuration_file))["pelicula"])

def database_read(opt:int, id:int):

    return get_film_list().read_like(opt, id)

def database_update(opt:int, data):

    return get_film_list().modify_like(opt, data)

def main_loop():
    
    opcio = None

    while opcio != '0':

        print("0.- Surt de l'aplicació.\n1.- Lectura de la base de dades\n2.- Inserta o Modifica una pel.licula\n")
        
        opcio = input("Selecciona una opció :\n")
                
        if opcio == '1':

            cls()

            last_id_handler = 0
            
            opt = int(input("0.- Lectura per any\n1.- Lectura de 10 en 10\n\nSelecciona un mètode per llegir-ho :\n"))
            
            cls()

            if (opt == 0): display_result(database_read(opt, last_id_handler))
            else: 

                cls()

                while input("\nPresiona ENTER si vols veure 10 pel.licules, si no 0\n") != '0':

                    last_10_films = database_read(opt, last_id_handler)

                    cls()

                    for film in last_10_films["films"]:
                        print(film)

                    last_id_handler = last_10_films["last_id"]

                cls()
                    

        elif opcio == '2':

            cls()

            opt = int(input("0.- Inserta una pel.licula\n1.- Modifica una pel.licula\n\nSelecciona una opció :\n"))

            input_text = " numero corresponent dels atributs que vols modificar del ordre (1, 2, 3, 4) " if opt == 1 else " " 
            
            cls()

            database_update(opt, input(f"Escriu per espais separats el{input_text}(titol, any, puntuacio, vots)\n").strip())


def main():

    print("\nBenvingut a la app de pel·lícules")
    input("Prem la tecla 'Enter' per a continuar\n")
    cls()

    main_loop()


if __name__ == "__main__":
    main()
