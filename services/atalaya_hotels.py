if __name__ == '__main__':
	from api_data_order import APIDataOrder,json,requests
	from ..utilities.utilities import lowercase_dictionary
else:
	from services.api_data_order import APIDataOrder,json,requests
	from utilities.utilities import lowercase_dictionary

hotel_atalaya_hotels = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'

hotel_atalaya_rooms = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'

hotel_atalaya_meals = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'

class AtalayaHotels(APIDataOrder):

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
		response = requests.get(self.url_rooms)
		json_response = response.json()
		return json_response

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
				'city':hotel['city'],
				'rooms':{}
			}
		return hotels_json

	def rooms_transformed(self):
		rooms = self.get_rooms()
		rooms_json = {}
		for room in rooms['rooms_type']:
			rooms_json[room['code']] = room['name']
		return rooms_json

	def conventional_order(self,hotels,code_rooms,meals):
		conventional_json = {}
		hotels_transformed = self.hotels_transformed()
		conventional_json["hotels"] = hotels_transformed["hotels"]

		for hotel_code in conventional_json['hotels'].keys():
			conventional_json['hotels'][hotel_code]['rooms'] = []

		for meal in meals['meal_plans']:
			for hotel in meal['hotel'].keys():
				for room in meal['hotel'][hotel]:
					conventional_json['hotels'][hotel]['rooms'].append({
						'name':code_rooms[room['room']],
						'room_type':room['room'],
						'meal_plan':meal['code'],
						'price':room['price']
					})
		for hotel in hotels['hotels']:
			hotel['rooms'] = conventional_json['hotels'][hotel['code']]['rooms']
			
		return hotels

	def conventional_dict(self):
		list_all_hotels = self.conventional_order()
		for hotel in list_all_hotels['hotels']:
			pass

	def dictionary_order(self):
		get_info_dev = {}
		get_info_dev = self.hotels_transformed()
		list_meals = self.get_meals()
		dict_rooms = self.rooms_transformed()
		for meal_plan in list_meals['meal_plans']:
			code_meal = meal_plan['code']
			name_meal = meal_plan['name']

			for hotel,rooms in meal_plan['hotel'].items():
				has_meal = get_info_dev['hotels'][hotel]['rooms'].get(code_meal)
				
				if has_meal == None:
					get_info_dev['hotels'][hotel]['rooms'][code_meal] = {}
				
				for room in rooms:
					code_room = room['room']
					price = room['price']
					room_name = dict_rooms[code_room]
					has_room = get_info_dev['hotels'][hotel]['rooms'][code_meal].get(code_room)
					
					if has_room == None:
						get_info_dev['hotels'][hotel]['rooms'][code_meal][code_room] = {}
					
					get_info_dev['hotels'][hotel]['rooms'][code_meal][code_room] = {
						'price':price,
						'meal_name':name_meal,
						'room_name':room_name
					}
		get_info_dev = lowercase_dictionary(get_info_dev)
		return get_info_dev

	def get_info(self):
		all_info_json = self.conventional_order(self.get_hotels(),self.rooms_transformed(),self.get_meals())
		return all_info_json

atalaya = AtalayaHotels(url_hotels=hotel_atalaya_hotels,url_rooms=hotel_atalaya_rooms,url_meals=hotel_atalaya_meals)
#print(atalaya.dictionary_order())
#print(atalaya.rooms_transformed())
#print("\n\n")
#print(atalaya.dictionary_order())
# dict_result = atalaya.dictionary_order()
# json_result = json.dumps(dict_result,indent=4)
# with open('../data/atalaya_dic.json','w') as file:
# 	file.write(json_result)