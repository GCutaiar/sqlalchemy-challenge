import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    """Available Routes"""
    return (f"Precipitation Analysis: /api/v1.0/precipitation <p>"
            f"Station List: /api/v1.0/stations <p>"
            f"Temperature Observation: /api/v1.0/stations <p>"
            f"Start and end range: /api/v1.0/&lt;start&gt;, /api/v1.0/&lt;start&gt;/&lt;end&gt; <p>"
        )

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)

    dates_last = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()

    dates_12 = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    all_prcp_dates = []
    for date, prcp in dates_12:
        rain_days = {}
        rain_days["date"] = date
        rain_days["prcp"] = prcp
        all_prcp_dates.append(rain_days)
    return jsonify(all_prcp_dates)

@app.route("/api/v1.0/stations")
def stat():
    session = Session(engine)

    stations = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    tobs_12 = session.query(Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').all()

    session.close()

    year_temps = list(np.ravel(tobs_12))

    return jsonify(year_temps)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    temp_query = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),\
        func.avg(Measurement.tobs)).filter(Measurement.date >=start).all()
  
    session.close()

    temp_results = list(np.ravel(temp_query))

    return jsonify(temp_results)
@app.route("/api/v1.0/<start>/<end>")
def range (start, end):
    session = Session(engine)

    temp_query = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),\
        func.avg(Measurement.tobs)).filter(Measurement.date >=start).\
            filter(Measurement.date <=end).all()
  
    session.close()

    temp_results = list(np.ravel(temp_query))

    return jsonify(temp_results)

if __name__ == "__main__":
    app.run(debug=True)
