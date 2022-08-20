from abc import abstractmethod
import requests, json

class APIDataOrder():

	group_of_apis = []

	def __init__(self,group_of_apis):
		self.group_of_apis = group_of_apis

	def show_all_info(self):
		list_info = {'hotels':[]}
		for api in self.group_of_apis:
			list_info['hotels'] += api.get_info()['hotels']
		return list_info
		
	@abstractmethod
	def conventional_order():
		pass

	@abstractmethod
	def get_hotels():
		pass

	@abstractmethod
	def get_rooms():
		pass

	@abstractmethod
	def get_meals():
		pass

