import ast
import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get('OWM_API_KEY')
MY_LAT = 30.748318
MY_LONG = 76.747047
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')
client = Client(account_sid, auth_token)

parameters = {
    'lat': MY_LAT,
    'lon': MY_LONG,
    'appid': API_KEY,
     'cnt': 4 #Will give us only 3 hours data,for four consecutive 3-hours chunk,not for 5 days/3hours chunk. as by default.
}

response = requests.get(OWM_ENDPOINT,params=parameters)

response.raise_for_status()

print('The status code for the request is:',response.status_code)

will_rain = False
for i in range(4):
    condition_code = response.json()['list'][i]['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True
        # weather_description = response.json()['list'][i]['weather'][0]['description']
print(response.json())

if will_rain:
    try:
        numbers = ast.literal_eval(os.environ.get('NUMBERS')) #to convert string to list.
        """
         Think of ast.literal_eval as a "Safe Python Translator." 
         It takes a string that looks like Python code (a "literal") and turns it into an actual Python object
         (like a list, dictionary, number, or tuple).
         """

        for number in numbers:
            sms_message = client.messages.create(
                body = 'Bring an umbrella!️☔',
                from_=os.environ.get('FROM'),
                to = number
            )
            print(sms_message.status)
    except Exception as ex:
        print(ex)
