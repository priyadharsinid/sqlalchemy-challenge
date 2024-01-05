# Import the dependencies.
import numpy as np 
import datetime as dt 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>(start:replace with star date,format:yyyy-mm-dd)<br/>"
        f"/api/v1.0/start/end<br/>(start:replace with star date, end:replace with end date,format:yyyy-mm-dd)<br/>"
      )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
     # Create our session (link) from Python to the DB
    session = Session(engine)
    

    """Return the last 12 months of precipitation data"""
   
    # Query recent date and last12months
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date=list(np.ravel(results_date))[0]
    recent_dt=dt.datetime.strptime(recent_date,"%Y-%m-%d")
    last12months = recent_dt-dt.timedelta(days=366)
   
    # Query date and prcp
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>= last12months).all()

    session.close()

    prcpdata=[]
    for date,prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcpdata.append(prcp_dict)

    return jsonify(prcpdata)

@app.route("/api/v1.0/stations")
def stations():
    #create session link from python to the Database
    session = Session(engine)
    
    
    """Return a list of all station """
     # Query all stations
    results = session.query(Station.station,Station.name).all()

    session.close()
      
    stations = {}
    for id,name in results:
        stations[id] = name
    return jsonify(stations)

    

@app.route("/api/v1.0/tobs")
def tobs():
    #create session link from python to the Database
    session = Session(engine)
   
    """Return the last 12 months of temparture observation data for active station """
      # Query recent date and last12months
    
    results_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date=list(np.ravel(results_date))[0]
    recent_dt=dt.datetime.strptime(recent_date,"%Y-%m-%d")
    last12months = recent_dt-dt.timedelta(days=365)

    #Query active station

    results_station = session.query(Measurement.station,
                              func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()
    active_station =list(np.ravel( results_station))[0]

     # Query date and tobs
    results= session.query(Measurement.date, Measurement.tobs).filter((Measurement.date>= last12months)
                           & (Measurement.station==active_station)).all()
  
    session.close()
    print(results)
    tobs=[]
    for date, temp in results:
        tobs_dict={}
        tobs_dict["date"]=date
        tobs_dict["tobs"]=temp
        tobs.append(tobs_dict)
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def startdate(start):    

    
    #create session link from python to the Database
    session = Session(engine)

    
    """Return Tmin,Tmax,Tavg"""
    #Query min.max,avg temp for startdate
    results=session.query(Measurement.date,func.min(Measurement.tobs), func.avg(Measurement.tobs), 
                          func.max(Measurement.tobs)). filter(Measurement.date >= start).\
                            group_by(Measurement.date).all()
                            
   
    session.close()
    
    start_list=[]
    for dt, min, avg, max in results:
        start_dict = {}
        start_dict["Date"] = dt
        start_dict["TMIN"] = min
        start_dict["TAVG"] = avg
        start_dict["TMAX"] = max
        start_list.append(start_dict)
    return jsonify(start_list)
    

@app.route("/api/v1.0/<start>/<end>")
def start_enddate(start,end):
   
    #create session link from python to the Database
    session = Session(engine)

    

    """Return Tmin,Tmax,Tavg"""
     #Query min.max,avg temp for startdate and enddate
    results= session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs), 
                         func.avg(Measurement.tobs)). filter(Measurement.date >= start).filter(Measurement.date <= end).\
                            group_by(Measurement.date).all()
    
    session.close()
    startend_list=[]
    for dt ,min, avg, max in results:
        startend_dict = {}
        startend_dict["Date"] = dt
        startend_dict["TMIN"] = min
        startend_dict["TAVG"] = avg
        startend_dict["TMAX"] = max
        startend_list.append(startend_dict)
    return jsonify(startend_list)

if __name__ =="__main__":
    app.run(debug=True)




