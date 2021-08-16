from flask import Flask, request, render_template, jsonify
import requests
import json
import logging
import datetime
import geocoder
import re


app = Flask(__name__)
logging.basicConfig(filename="info.log", level=logging.INFO)


def save_to_json(date):
    json_file = open("date.json", mode="r", encoding="Latin-1")
    old_json = json.load(json_file)
    json_file.close()
    old_json.update(date)
    json_file = open("date.json", mode="w", encoding="Latin-1")
    json.dump(old_json, json_file)
    json_file.close()


def get_location(ip):

    location_url = f"http://ipinfo.io/{ip}/json"
    response = requests.get(location_url)
    date = response.json()
    print("getLocation")
    return {
        "ip": date.get("ip", ""),
        "country": date.get("country", ""),
        "region": date.get("region", ""),
        "city": date.get("city", ""),
        "hostname": date.get("hostname", ""),
        "location": date.get("loc", ""),
        "postal code": date.get("postal", "")
    }


@app.route("/", methods=["GET"])
def get_my_ip():
    headers_list = request.headers.getlist("X-Forwarded-For")
    user_ip = headers_list[0] if headers_list else request.remote_addr
    # user_ip = request.remote_addr
    all_data = request.environ
    date = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    breakpoint()
    need_info = {
        date: {
            "ip": all_data.get("REMOTE_ADDR"),
            "user_port": all_data.get("REMOTE_PORT"),
            "user_agent": all_data.get("HTTP_USER_AGENT")
        }
    }
    location = get_location(user_ip)
    need_info[date].update(location)
    save_to_json(need_info)
    return jsonify(need_info)
    # return render_template('blog/index.html')


if __name__ == '__main__':
    app.run()
