from abc import abstractmethod
import requests, json
import copy

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

	def book_best_hotel(self,input_bookings):
		def downgrade_booking(index,bookings):
			booking_meal_plan = bookings[index]['meal_plan']
			booking_room_type = bookings[index]['room_type']
			meal_plans = {'sa':0,'ad':1,"mp":2,'pc':3}
			meal_plans_inv = {v: k for k,v in meal_plans.items()}#{0: 'sa', 1: 'ad', 2: 'mp', 3: 'pc'}
			meal_plans_length = len(meal_plans_inv)
			room_types = {'standard':0,'suite':1}
			room_types_inv = {v: k for k,v in room_types.items()}

			booking_meal_plan_priority = meal_plans[booking_meal_plan]
			booking_room_type_priority = room_types[booking_room_type]
			if  booking_meal_plan_priority > 0:
				bookings[index]['meal_plan'] = meal_plans_inv[booking_meal_plan_priority-1]
			else:
				if booking_room_type_priority > 0:
					bookings[index]['room_type'] = room_types_inv[booking_room_type_priority-1]
					bookings[index]['meal_plan'] = meal_plans_inv[meal_plans_length-1]

		dict_all_hotels = self.show_all_dict()
		bookings_copy = copy.deepcopy(input_bookings)
		budget = bookings_copy['budget']
		persons = bookings_copy['persons']
		finished = False
		while finished is not True:
			budget_left = budget
			for index,booking in enumerate(bookings_copy['bookings']):
				booking_hotel_code = booking['hotel_code']
				booking_nights = booking['nights']
				booking_room_type = booking['room_type']
				booking_meal_plan = booking['meal_plan']
				room_meal_price = dict_all_hotels['hotels'][booking_hotel_code]['rooms'][booking_meal_plan][booking_room_type]['price']
				total_cost = room_meal_price * booking_nights * persons
				budget_left -= total_cost
				if budget_left < 0:
					if booking_room_type == 'standard' and booking_meal_plan == 'sa':
						if index == 0:
							print("no te puedes permitir reservr nada, lo sentimos")
							finished = True
							break
						else:
							downgrade_booking(index-1,bookings_copy['bookings'])
							bookings_copy['bookings'][index] = input_bookings['bookings'][index]
							break
					else:
						print("no te lo puedes permitir, buscando opcion mas adecuada...")
						downgrade_booking(index,bookings_copy['bookings'])
						break
					
				else:
					if index+1 >= len(bookings_copy['bookings']):
						finished = True
						break
		return bookings_copy
						
		#Ejemplo de lo que llegará como dato
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

