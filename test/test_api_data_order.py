import requests
from services.atalaya_hotels import AtalayaHotels

hotel_atalaya_hotels = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'
hotel_atalaya_rooms = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'
hotel_atalaya_meals = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'

atalaya = AtalayaHotels(url_hotels=hotel_atalaya_hotels,url_rooms=hotel_atalaya_rooms,url_meals=hotel_atalaya_meals)

def test_create_atalaya_api():
	assert len(atalaya.url_hotels) > 0
	assert len(atalaya.url_meals) > 0
	assert len(atalaya.url_rooms) > 0

def test_get_hotels_status():
	response = requests.get(atalaya.url_hotels)
	status_code = response.status_code
	assert status_code == 200

def test_get_rooms_status():
	response = requests.get(atalaya.url_rooms)
	status_code = response.status_code
	assert status_code == 200

def test_get_meals_status():
	response = requests.get(atalaya.url_meals)
	status_code = response.status_code
	assert status_code == 200

def test_get_hotels_json():
	json_hotels = atalaya.get_hotels()
	list_hotels = json_hotels['hotels']
	list_of_codes = []
	for reg in list_hotels:
		code_hotel = reg['code']
		list_of_codes.append(code_hotel)
	assert set(list_of_codes) == set(['ave','acs'])

def test_get_rooms_json():
	json_rooms = atalaya.get_rooms()
	list_rooms = json_rooms['rooms_type']
	list_of_codes = []
	for reg in list_rooms:
		code_room = reg['code']
		list_of_codes.append(code_room)
	assert set(list_of_codes) == set(['standard','suite'])

def test_get_meals_json():
	json_meals = atalaya.get_meals()
	list_meals = json_meals['meal_plans']
	list_of_codes = []
	for reg in list_meals:
		code_meal = reg['code']
		list_of_codes.append(code_meal)
	assert set(list_of_codes) == set(['pc','mp','ad','sa'])

def test_get_info():
	json_info = atalaya.get_info()
	list_hotels = json_info['hotels']
	city = list_hotels[0]['city']
	code = list_hotels[0]['code']
	name = list_hotels[0]['name']
	rooms = list_hotels[0]['rooms']
	assert isinstance(list_hotels,list) == True
	assert isinstance(city,str) == True
	assert isinstance(code,str) == True
	assert isinstance(name,str) == True
	assert isinstance(rooms,list) == True

def test_dictionary_order():
	json_info = atalaya.dictionary_order()
	dict_hotels = json_info['hotels']
	city = ''
	name = ''
	rooms = {}
	for reg in dict_hotels.keys():
		city = dict_hotels[reg]['city']
		name = dict_hotels[reg]['name']
		rooms = dict_hotels[reg]['rooms']
		break #solo queremos el primer registro da igual el orden
	assert isinstance(dict_hotels,dict) == True
	assert isinstance(city,str) == True
	assert isinstance(reg,str) == True
	assert isinstance(dict_hotels[reg],dict) == True
	assert isinstance(name,str) == True
	assert isinstance(rooms,dict) == True


