import sys
from services.atalaya_hotels import AtalayaHotels
from services.resort_hotels import ResortHotels
from services.api_data_order import APIDataOrder
import json
from flask import Flask, request as flask_request


api_hotels_atalaya = AtalayaHotels(url_hotels='http://www.mocky.io/v2/5e4a7e4f2f00005d0097d253',url_rooms='https://run.mocky.io/v3/132af02e-8beb-438f-ac6e-a9902bc67036',url_meals='http://www.mocky.io/v2/5e4a7e282f0000490097d252')

api_hotels_resort = ResortHotels(url_hotels='http://www.mocky.io/v2/5e4e43272f00006c0016a52b',url_meals='http://www.mocky.io/v2/5e4a7dd02f0000290097d24b')

api_data_order = APIDataOrder([api_hotels_atalaya,api_hotels_resort])

json_result = api_data_order.show_all_info()

json_result = json.dumps(json_result, indent=4)

# el Punto 1 Entero Hecho
if __name__ == '__main__':
	try:
		with open("./data/result.json", "w") as outfile:
			outfile.write(json_result)
	except:
		pass

#el punto 2
app = Flask(__name__)

@app.route('/listar-hoteles-atalaya')
def list_atalaya_hotels():
    return api_hotels_atalaya.get_info()

@app.route('/listar-hoteles-resort')
def list_resort_hotels():
	return api_hotels_resort.get_info()

@app.route('/listar-todos-los-hoteles')
def list_all_hotels():
	return api_data_order.show_all_info()

@app.route('/listar-todos-los-hoteles-desarollo')
def list_all_hotels_dict():
	return api_data_order.show_all_dict()

@app.route('/listar-mejor-hotel', methods=['GET'])
def list_best_hotel():
	bookings = flask_request.json
	return api_data_order.book_best_hotel(bookings)

if __name__ == '__main__':
	try:
		if sys.argv[1] == "production":
			app.run(debug=False, use_debugger=False,host='0.0.0.0')
	except IndexError:
		app.run(debug=True, use_debugger=True,host='0.0.0.0')