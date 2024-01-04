# Import the dependencies.
from flask import Flask, jsonify
import numpy as np 
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

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
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
      )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of all precipitation and date"""
    
    ppt = session.query(measurement.date,measurement.prcp).all()

    session.close()

    prcpdata=[]
    for date,prcp in ppt:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcpdata.append(prcp_dict)

    return jsonify(prcpdata)

@app.route("/api/v1.0/stations")
def stations():
    #create session link from python to the Database
    session = Session(engine)
    list_stations = session.query(measurement.station).distinct().all()

    session.close()

    all_stations=list(np.ravel(list_stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link from python to the Database
    session = Session(engine)
    last12months = dt.date(2017,8,23)-dt.timedelta(days=365)
    stationdata = session.query(measurement.date, measurement.tobs).filter((measurement.date>= last12months) & (measurement.station=="USC00519281")).all()
  
    session.close()

    all_tobs=list(np.ravel(stationdata))
    return jsonify(all_tobs)



if __name__ =="__main__":
    app.run(debug=True)




