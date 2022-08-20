from api_data_order import APIDataOrder,json,requests

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
			
		return hotels

	def get_info(self):
		all_info_json = self.conventional_order(self.get_hotels(),self.rooms_transformed(),self.get_meals())
		return all_info_json

api_hotels_resort = ResortHotels(url_hotels='http://www.mocky.io/v2/5e4e43272f00006c0016a52b',url_meals='http://www.mocky.io/v2/5e4a7dd02f0000290097d24b')

hoteles_resort = api_hotels_resort.get_hotels()
habitaciones_resort = api_hotels_resort.get_rooms()
regimenes_resort = api_hotels_resort.get_meals()

hoteles_resort_transformed = api_hotels_resort.hotels_transformed()

get_info_resort = api_hotels_resort.get_info()
# print("hoteles\n",hoteles_resort)
# print("habitaciones\n",habitaciones_resort)
# print("regimenes\n",regimenes_resort)
# print("hoteeles transformado\n",hoteles_resort_transformed)
# print(get_info_resort)

get_info_resort = json.dumps(get_info_resort, indent=4)
 
# Writing to sample.json
with open("sample2.json", "w") as outfile:
    outfile.write(get_info_resort)