#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def hello_world():
#    return 'Hello World'
#
## http://127.0.0.1:5000/

#Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify 

#Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

#Reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session (engine)

#Set Up Flask
app = Flask(__name__)

#Define the welcome route
@app.route("/")
def welcome():
    return(

    '''

    Welcome to the Climate Analysis API! <br>

    Available Routes: <br>

    /api/v1.0/precipitation <br>

    /api/v1.0/stations <br>

    /api/v1.0/tobs <br>

    /api/v1.0/temp/start/end
    
    ''')

#create the precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#create the Stations Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

