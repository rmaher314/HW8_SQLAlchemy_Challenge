# Import Dependencies
import numpy as np

#import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

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
        f"/api/v1.0/<'start'><br/>"
        f"/api/v1.0/<'start'>/<'end'><br/>"
    )

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations in Data set"""
    # Query all passengers
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



if __name__ == '__main__':
    app.run(debug=True)