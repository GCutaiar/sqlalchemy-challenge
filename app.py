from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "Routes Available"
    # declare available routes

@app.route("/api/v1.0/Precipitation")
def prcp():
    return # JSON dictionary of query {date:prcp}

@app.route("/api/v1.0/Stations")
def stat():
    return #JSON list of station names and numbers

@app.route("/api/v1.0/TOBS")
def tobs():
    return #query dates and temps from previous year
        #return JSON list of Temperature Observations

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
# if start or start-end date entered, JSON list TMIN,TAVG,TMAX
# if only start, calculate TMIN, TAVG, TMAX all dates>=start date
# if both start and end, TMIN, TAVG, TMIN between dates including end points

if __name__ == "__main__":
    app.run(debug=True)
