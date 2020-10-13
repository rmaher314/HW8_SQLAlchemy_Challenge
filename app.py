# Import Dependencies
import numpy as np

#import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Import Dependencies

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link)
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<'start'><br/>"
        f"/api/v1.0/start_end/<'start'>/<'end'><br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations in Data set"""
    # Query all Stations
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    """Convert the query results to a dictionary using 'date' as the key and 'prcp' as the value"""
    # Query all passengers
    all_dates = []
    for date, prcp in results:
        date_dict = {}
        date_dict["date"] = date
        date_dict["prcp"] = prcp
        all_dates.append(date_dict)   
    return jsonify(all_dates)

@app.route("/api/v1.0/start/<start>")
def start(start):
    # Date format for searching should be MM-DD-YYY
    
    date_obj = dt.datetime.strptime(start, '%m-%d-%Y')
    session = Session(engine)

    # Query most active station
    #,Measurement.tobs, Measurement.date, Measurement.tobs)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= date_obj).all()
        

    session.close()

    return jsonify(results)
    # Convert list of tuples into normal list

    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    date = dt.datetime(2016, 8, 22)
    session = Session(engine)

    # Query most active station and the last 12 months of data.  
    # #Since I queried the active station the first half of the assignment I wnent ahead and hard coded that into this side of the assignment.
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date >= date).all()

    session.close()

    # Convert list of tuples into normal list

    return jsonify(results)

@app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start,end):
    start_date_obj = dt.datetime.strptime(start, '%m-%d-%Y')
    end_date_obj = dt.datetime.strptime(end, '%m-%d-%Y')
    # Date format for searching should be MM-DD-YYY

    session = Session(engine)

    # Query the min, maximum and averages between two sets of dates.  
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date_obj).\
        filter(Measurement.date <= end_date_obj).all()

    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)