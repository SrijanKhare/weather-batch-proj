import requests
import json

api_key = ''
base_curr_cond_url = 'http://api.weatherapi.com/v1/forecast.json'



def get_lat_longs(json_file: str):
	f = open(input_cities_file)
	cities_json = json.load(f)
	coord_list = [(row['latitude'], row['longitude']) for row in cities_json]
	return coord_list

def write_to_file(json_list, target_file):
	json.dump(json_list, target_file, indent = 6)

def get_data(target_file: str, input_cities_file: str) -> None:
	coord_list = get_lat_longs(input_cities_file)

	for coord in coord_list:
		lat = coord[0]
		lon = coord[1]
		url = base_url + 'key=' + api_key + +str(lat)+','+str(long)+'&days=1&aqi=no&alerts=yes'

		json_list = []
		r = requests.get(url)
		json_list.append(r.json())

		write_to_file(json_list, target_file)




