import requests
from datetime import datetime
import smtplib
import time


MY_EMAIL = "your_email"
PASSWORD = "your_pass"
TO_MAIL = "your_email"
MY_LAT = "your_lat"
MY_LONG = "your_long"


def poistion_in():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LONG - 5 < iss_longitude < MY_LONG + 5:
        if MY_LAT - 5 < iss_latitude < MY_LAT + 5:
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
    # print(sunrise, sunset)

    time_now = datetime.now().hour
    if time_now < sunrise or time_now > sunset:
        return True


while True:
    time.sleep(60)
    if poistion_in() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_MAIL,
            msg="Subject:Look Up\n\n The ISS is above you in your head in the sky."
        )





