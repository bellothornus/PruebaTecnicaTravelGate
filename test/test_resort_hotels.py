import requests
from services.resort_hotels import ResortHotels

hotel_resort_hotels = 'http://www.mocky.io/v2/5e4e43272f00006c0016a52b'
hotel_resort_meals = 'http://www.mocky.io/v2/5e4a7dd02f0000290097d24b'

atalaya = ResortHotels(url_hotels=hotel_resort_hotels,url_rooms=hotel_resort_hotels,url_meals=hotel_resort_meals)

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
	assert set(list_of_codes) == set(['hrc','hrm'])

def test_get_rooms_json():
	json_rooms = atalaya.get_rooms()
	dict_rooms = json_rooms['hotels']
	list_of_codes = []
	for reg in dict_rooms.keys():
		list_rooms = dict_rooms[reg]
		for room in list_rooms:
			code_room = room['code']
			list_of_codes.append(code_room)
	assert set(list_of_codes) == set(['st','su'])

def test_get_meals_json():
	json_meals = atalaya.get_meals()
	list_meals = json_meals['regimenes']
	for reg in list_meals:
		code_meal = reg['code']
		name_meal = reg['name']
		hotel_meal = reg['hotel']
		room_type = reg['room_type']
		price = reg['price']
		break
	assert isinstance(code_meal,str) == True
	assert isinstance(name_meal,str) == True
	assert isinstance(hotel_meal,str) == True
	assert isinstance(room_type,str) == True
	assert isinstance(price,int) == True

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


