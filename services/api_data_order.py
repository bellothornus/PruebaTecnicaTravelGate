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
		
	def show_all_dict(self):
		list_info = {'hotels':{}}
		for api in self.group_of_apis:
			list_info['hotels'].update(api.dictionary_order()['hotels'])
		return list_info

	def book_best_hotel(self,bookings,budget,persons):
		def downgrade_booking(index,bookings):
			booking = bookings[index]
			booking_meal_plan = booking['meal_plan']
			booking_room_type = booking['room_type']
			meal_plans = {'sa':0,'ad':1,"mp":2,'pc':3}
			meal_plans_inv = {v: k for k,v in meal_plans.items()}#{0: 'sa', 1: 'ad', 2: 'mp', 3: 'pc'}
			meal_plans_length = len(meal_plans_inv)
			room_types = {'standard':0,'suite':1}
			room_types_inv = {v: k for k,v in room_types.items()}

			booking_meal_plan_priority = meal_plans[booking_meal_plan]
			booking_room_type_priority = room_types[booking_room_type]
			if  booking_meal_plan_priority > 0:
				booking_meal_plan = meal_plans_inv[booking_meal_plan_priority-1]
			else:
				if booking_room_type_priority > 0:
					booking_room_type = room_types_inv[booking_meal_plan_priority-1]
					booking_meal_plan = meal_plans_inv[meal_plans_length-1]

		dict_all_hotels = self.show_all_dict()
		bookings_copy = bookings.copy()
		finished = False
		while finished is not True:
			for index,booking in enumerate(bookings_copy['bookings']):
				booking_hotel_code = booking['hotel_code']
				booking_nights = booking['nights']
				booking_room_type = booking['room_type']
				booking_meal_plan = booking['meal_plan']
				room_meal_price = dict_all_hotels['hotels'][booking_hotel_code]['rooms'][booking_meal_plan][booking_room_type]['price']
				total_cost = room_meal_price * booking_nights * persons
				budget_left = budget - total_cost
				if budget_left < 0:
					print("no te lo puedes permitir, buscando opcion mas adecuada...")
					downgrade_booking(index,bookings_copy['bookings'])
					if booking_room_type == 0 and booking_meal_plan == 0:
						if index == 0:
							print("no te puedes permitir reservr nada, lo sentimos")
				else:
					if index+1 >= len(booking):
						finished = True
						break
		return bookings_copy
						


		# list_all_hotels = self.show_all_info()
		# book_aux = {}
		# list_made_bookings = []
		# for book in bookings['bookings']:
		# 	book_aux = {
		# 		'meal_plan':book['meal_plan'],
		# 		'room_type':book['room_type']
		# 	}
		# 	for hotel in list_all_hotels['hotels']:
		# 		if hotel['code'] == book['hotel_code']:
		# 			for room in hotel['rooms']:
		# 				if room['meal_plan'] == book['meal_plan'] and room['room_type'] == room['room_type']:
		# 					cost = room['price']*book['nights'] * persons
		# 					budget_left = budget - cost
		# 					if budget_left > -1:
		# 						list_made_bookings.append({
		# 							'meal_plan':room['meal_plan'],
		# 							'name': room['name'],
		# 							'price': cost,
		# 							'room_type': room['room_type'],
		# 							'nights':book['nights']
		# 						})
		# 					else:
		# 						self.downgrade_book(book)
		# {
		# 	'bookings':[
		# 		{
		# 			'hotel_code':'acs'
		# 			'days':3,
		# 			'room_type':'suite',
		# 			'meal_plan';'pc'
		# 		},
		# 		{
		# 			'hotel_code':'hrc',
		# 			'days':5,
		# 			'room_type':'standard',
		# 			'meal_plan':'ad'
		# 		}
		# 	]
		# }
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

	def add_api(self,api):
		self.group_of_apis.append(api)

