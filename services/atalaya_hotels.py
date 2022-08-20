from api_data_order import APIDataOrder,json,requests

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
				'city':hotel['city']
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

	def get_info(self):
		all_info_json = self.conventional_order(self.get_hotels(),self.rooms_transformed(),self.get_meals())
		return all_info_json

api_hotels_atalaya = AtalayaHotels(url_hotels='http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253',url_rooms='https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036',url_meals='http://www.mocky.io/v2/5e4a7e282f0000490097d252')

hoteles_atalaya = api_hotels_atalaya.get_hotels()
habitaciones_atalaya = api_hotels_atalaya.get_rooms()
regimenes_atalaya = api_hotels_atalaya.get_meals()

hoteles_atalaya_transformed = api_hotels_atalaya.hotels_transformed()

get_info_atalaya = api_hotels_atalaya.get_info()
# print("hoteles\n",hoteles_atalaya)
# print("habitaciones\n",habitaciones_atalaya)
# print("regimenes\n",regimenes_atalaya)
# print("hoteeles transformado\n",hoteles_atalaya_transformed)
print(get_info_atalaya)

get_info_atalaya = json.dumps(get_info_atalaya, indent=4)
 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(get_info_atalaya)