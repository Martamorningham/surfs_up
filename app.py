#####Flask for Surfs up
# import dependencies for weather app 
import datetime as dt
import numpy as np
import pandas as pd

#import sqlalchemy 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask 
from flask import Flask, jsonify

#####set up DB
#connect to hawaii sqlite  
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect db into classes
#reflect tables
Base = automap_base()
#reflect db 
Base.prepare(engine, reflect=True)

#create variabels for each classe
Measurement = Base.classes.measurement
Station = Base.classes.station

# create session link from python to DB
session = Session(engine)


##### set up flask
#create app define flaskapp
app = Flask(__name__)

#check that app is working 
import app
print("example __name__ = %s", __name__)

if __name__ == "__main__":
	print("example is being run directly.")
else:
	print("example is being imported")

# Define the Flask app
app = Flask(__name__)


#define welcome welcome route
@app.route("/")

#add route info using f strings to display percipitation, stations, tobs, and temp routes 
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

##create percipitation app
#define app route
@app.route("/api/v1.0/precipitation")

#create percipitation funciotn 
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

##create staations route 
@app.route("/api/v1.0/stations")
#create stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

##create tobs route
@app.route("/api/v1.0/tobs")

#create temp_monthly function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

##create stats route for min, max, avg
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

#create stats function
#create perameters for stats start & end 
#create list for query
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
