import requests
import datetime as dt
from twilio.rest import Client

account_sid = "xxxxxxxxxx"
auth_token = "xxxxxxxxxx"

SHEET_URL = "https://api.sheety.co/xxxxxxxxxx/flightDeals/prices"

sheet_response = requests.get(url=SHEET_URL).json()['prices']

FLIGHT_API = "xxxxxxxxxx"
FLIGHT_URL = "https://tequila-api.kiwi.com/v2/search"
header = {
    "apikey": FLIGHT_API
}
count = 2
for flight in sheet_response:
    x_year = dt.datetime.now().year
    x_day = dt.datetime.now().day
    x_month = dt.datetime.now().month
    my_flight_params = {
        "fly_from": "DEL",
        "fly_to": flight['iataCode'],
        "date_from": dt.datetime.now().strftime("%d/%m/%Y"),
        "date_to": dt.datetime(year=x_year + (x_month + 6) // 12, month=(x_month + 6) % 12, day=x_day).strftime(
            "%d/%m/%Y"),
        "flight_type": "oneway",
        "partner_market": "in",
        "curr": "INR",
        "limit": "1"
    }
    flight_data = requests.get(url=FLIGHT_URL, headers=header, params=my_flight_params)
    if int(flight_data.json()['data'][0]['price']) < int(flight["lowestPrice"]):
        flight["lowestPrice"] = flight_data.json()['data'][0]['price']
        flight['departure'] = flight_data.json()['data'][0]['local_departure']
        change_param = {
            "price": {
                "lowestPrice": flight["lowestPrice"]
            }
        }
        requests.put(url=f"https://api.sheety.co/xxxxxxxxxx/flightDeals/prices/{count}",
                     json=change_param)
    print(flight_data.json()['data'][0]['price'])
    count += 1

low = sheet_response[0]
for sheet in sheet_response:
    if int(low['lowestPrice']) > int(sheet['lowestPrice']):
        low = sheet
client = Client(account_sid, auth_token)
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f"Low Price Alert!!!\nOnly ₹{low['lowestPrice']} to fly from Delhi to {low['city']} on {low['departure'][:10]}",
    to='whatsapp:+91xxxxxxxxxx'
)
print(sheet_response)
