from abc import abstractmethod
import requests, json

class APIDataOrder():

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
