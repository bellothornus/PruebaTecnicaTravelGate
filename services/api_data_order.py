from abc import abstractmethod
import requests

hotel_atalaya_hotels = 'http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253'

hotel_atalaya_rooms = 'https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036'

hotel_atalaya_meals = 'http://www.mocky.io/v2/5e4a7e282f0000490097d252'

response = requests.get(hotel_atalaya_hotels)

print(response.json())

class APIDataOrder():

	@abstractmethod
	def get_hotels():
		pass

	@abstractmethod
	def get_rooms():
		pass

	@abstractmethod
	def get_meals():
		pass


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
