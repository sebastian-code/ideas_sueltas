import json
import requests

films_url = "https://ghibliapi.herokuapp.com/films"
people_url = "https://ghibliapi.herokuapp.com/people"
locations_url = "https://ghibliapi.herokuapp.com/locations"
species_url = "https://ghibliapi.herokuapp.com/species"
vehicles_url = "https://ghibliapi.herokuapp.com/vehicles"


def get_ghibli_data(url):
    return requests.get(url).text


films = json.loads(get_ghibli_data(films_url))
people = json.loads(get_ghibli_data(people_url))
locations = json.loads(get_ghibli_data(locations_url))
species = json.loads(get_ghibli_data(species_url))
vehicles = json.loads(get_ghibli_data(vehicles_url))

[print("Titulo: ", i["title"], " - Director: ", i["director"]) for i in films]
