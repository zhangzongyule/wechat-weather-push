import requests
import datetime
import random
import os

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
OPENID = os.getenv("OPENID")
HEFENG_KEY = os.getenv("HEFENG_KEY")
CITY_CODE = os.getenv("CITY_CODE")


def get_access_token():
    url = (
        "https://api.weixin.qq.com/cgi-bin/token"
        f"?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    )
    return requests.get(url).json()["access_token"]


def get_weather():
    url = (
        "https://devapi.qweather.com/v7/weather/now"
        f"?location={CITY_CODE}&key={HEFENG_KEY}"
    )
    now = requests.get(url).json()["now"]
    return now["text"], now["temp"]


def get_quote(weather_text):
    weekday = datetime.datetime.now().weekday()

    rain = [
        "雨会停的，你也是。",
        "下雨天，记得对自己温柔一点。"
    ]
    monday = [
        "今天不必完美，只要开始。",
    ]
    normal = [
        "慢一点没关系，但别停。",
        "你已经做得很好了。",
    ]

    if "雨" in weather_text:
        return random.choice(rain)
    if weekday == 0:
        return random.choice(monday)
    return random.choice(normal)


def send_message(token, weather, temp, quote):
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"

    data = {
        "touser": OPENID,
        "template_id": TEMPLATE_ID,
        "data": {
            "weather": {"value": weather},
            "temp": {"value": f"{temp}℃"},
            "quote": {"value": quote}
        }
    }

    requests.post(url, json=data)


def main():
    token = get_access_token()
    weather, temp = get_weather()
    quote = get_quote(weather)
    send_message(token, weather, temp, quote)


if __name__ == "__main__":
    main()
