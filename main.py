import smtplib
import requests
from datetime import datetime
import time

EMAIL = "EMAIL"
PASSWORD = "PASSWORD"
MY_LAT = 25.761681
MY_LONG = -80.191788

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()


time_now = datetime.now()
hours = time_now.hour
#Your position is within +5 or -5 degrees of the ISS position.


def is_it_overhead():

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG -5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    while True:
        time.sleep(60)
        if is_it_overhead() and is_night():
            connection = smtplib.SMTP("SMTP ADDRESS", port="PORT")
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs="OTHER_EMAIL", msg="Hello\n\nLook up to the sky to see the ISS")
            print("Email sent")