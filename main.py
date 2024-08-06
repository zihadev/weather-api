# coding=utf-8
import random
from flask import Flask, render_template
import data_processing as data_processing

app = Flask(__name__)


@app.route("/")
def home():
    # minimum_date = data_processing.start_date
    # maximum_date = data_processing.end_date
    minimum_date = "1860-01-01"
    maximum_date = "2022-05-31"
    stations_list = data_processing.stations_list()
    stations_table = stations_list[0:1000].to_html()
    print(len(stations_list))
    return render_template("home.html", minimum_date=minimum_date,
                           maximum_date=maximum_date,
                           stations_number=len(stations_list),
                           stations_table=stations_table)


@app.route("/api/v1/<station>/<date>")
def api(station, date):
    temperature = random.randint(-50, 50)
    if len(str(date)) != 8:
        info = "bad date"
        return {"info": info
                }
    else:

        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        formatted_station = int(station)
        temp = data_processing.check_api(date=formatted_date,
                                         station=formatted_station)

        return {

            "station": station,
            "date": date,
            "temp": temp,
            "formatted date ": formatted_date,
        }


@app.route("/api/v1/<station>")
def all_data(station):
    data = data_processing.station_data(station)
    return data


@app.route("/api/v2/<station>/<year>")
def year_data(station, year):
    data = data_processing.year_data(station, year)
    return data


if __name__ == "__main__":
    app.run(debug=True)
