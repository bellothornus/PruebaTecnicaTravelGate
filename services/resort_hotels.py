if __name__ == '__main__':
	from api_data_order import APIDataOrder,json,requests
	from ..utilities.utilities import lowercase_dictionary
else:
	from services.api_data_order import APIDataOrder,json,requests
	from utilities.utilities import lowercase_dictionary

hotel_resort_hotels = 'http://www.mocky.io/v2/5e4e43272f00006c0016a52b'

hotel_resort_meals = 'http://www.mocky.io/v2/5e4a7dd02f0000290097d24b'

class ResortHotels(APIDataOrder):

	url_hotels = ''
	url_rooms = ''
	url_meals = ''

	def __init__(self, **urls):
		for parameter,value in urls.items():
			setattr(self,parameter,value)

	def get_hotels(self):
		response = requests.get(self.url_hotels)
		json_response = response.json()
		return json_response
	
	def get_rooms(self):
		response = requests.get(self.url_hotels)
		json_response = response.json()
		rooms = {'hotels':{}}
		for hotel in json_response['hotels']:
			rooms['hotels'][hotel['code']] = []
			for room in hotel['rooms']:
				rooms['hotels'][hotel['code']].append({
					'code':room['code'],
					'name':room['name']
				})
		return rooms

	def get_meals(self):
		response = requests.get(self.url_meals)
		json_response = response.json()
		return json_response

	def hotels_transformed(self):
		hotels = self.get_hotels()
		hotels_json = {'hotels':{}}
		for hotel in hotels['hotels']:
			hotels_json['hotels'][hotel['code']] = {
				'name':hotel['name'],
				'city':hotel['location'],
				'rooms':{}
			}
		return hotels_json

	def rooms_transformed(self):
		rooms = self.get_rooms()
		rooms_json = {}
		for hotel in rooms['hotels']:
			for room in rooms['hotels'][hotel]:
				rooms_json[room['code']] = room['name']
		return rooms_json

	def conventional_order(self,hotels,code_rooms,meals):
		conventional_json = {}
		hotels_transformed = self.hotels_transformed()
		conventional_json["hotels"] = hotels_transformed["hotels"]

		for hotel_code in conventional_json['hotels'].keys():
			conventional_json['hotels'][hotel_code]['rooms'] = []

		for meal in meals['regimenes']:
			hotel = meal['hotel']
			room_type = meal['room_type']
			room_name = code_rooms[room_type]
			meal_plan = meal['code']
			price = meal['price']
			conventional_json['hotels'][hotel]['rooms'].append({
				'name':room_name,
				'room_type':room_type,
				'meal_plan':meal_plan,
				'price':price
			})
		for hotel in hotels['hotels']:
			hotel['rooms'] = conventional_json['hotels'][hotel['code']]['rooms']
			hotel['city'] = hotel['location']
			del hotel['location']
			
		return hotels

	def dictionary_order(self):
		get_info_dev = {}
		get_info_dev = self.hotels_transformed()
		list_meals = self.get_meals()
		dict_rooms = self.rooms_transformed()
		for meal_plan in list_meals['regimenes']:
			code_meal = meal_plan['code']
			name_meal = meal_plan['name']
			code_room = meal_plan['room_type']
			hotel = meal_plan['hotel']
			price = meal_plan['price']
			room_name = dict_rooms[code_room]
			has_meal = get_info_dev['hotels'][hotel]['rooms'].get(code_meal)
			if has_meal == None:
				get_info_dev['hotels'][hotel]['rooms'][code_meal] = {}
			
			has_room = get_info_dev['hotels'][hotel]['rooms'][code_meal].get(room_name)
			if has_room == None:
				get_info_dev['hotels'][hotel]['rooms'][code_meal][room_name] = {}
			
			get_info_dev['hotels'][hotel]['rooms'][code_meal][room_name] = {
						'price':price,
						'meal_name':name_meal,
						'room_name':room_name
					}
		get_info_dev = lowercase_dictionary(get_info_dev)
		return get_info_dev

	def get_info(self):
		all_info_json = self.conventional_order(self.get_hotels(),self.rooms_transformed(),self.get_meals())
		return all_info_json

resort = ResortHotels(url_hotels=hotel_resort_hotels,url_rooms=hotel_resort_hotels,url_meals=hotel_resort_meals)
#print(resort.dictionary_order())
#print(resort.rooms_transformed())
#print("\n\n")
#print(resort.dictionary_order())
# dict_result = resort.dictionary_order()
# json_result = json.dumps(dict_result,indent=4)
# with open('../data/resort_dic.json','w') as file:
# 	file.write(json_result)