# Import the dependencies.
import numpy as np
import flask 
print(flask.__version__)
import sqlalchemy
print(sqlalchemy.__version__)
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
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Stations = Base.classes.station

# Create our session (link) from Python to the DB
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

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine) 

    sel = [Measurements.date, Measurements.prcp]
    precip_data = session.query(*sel).filter(Measurements.date >= "2016-08-23").all()

    session.close()

    precip_dic = dict(precip_data)

    return jsonify(precip_dic)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine) 

    station_num = session.query(Measurements.station).group_by(Measurements.station).all()

    session.close()

    station_list = []

    for i in range(len(station_num)):
        station_list.append(station_num[i][0])
    

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine) 

    sel = [Measurements.tobs]
    waihee_station = session.query(*sel).filter(Measurements.station == "USC00519281").filter(Measurements.date >= "2016-08-23").all()
    
    session.close()

    tobs_list = []

    for i in range(len(waihee_station)):
        tobs_list.append(waihee_station[i][0])

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def date_summary(start):
    session = Session(engine)

    start_date = start
    summary = session.query(Measurements.date, func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).filter(Measurements.date >= start_date).group_by(Measurements.date).all()
    
    session.close() 

    summary_list = []

    for i in range(len(summary)):
        summary_list.append(summary[i][1:])

    return jsonify(summary_list)


# /api/v1.0/"2016-06-23"/"2016-09-23"
@app.route("/api/v1.0/<start>/<end>")
def time_frame_summary(start,end):
    session = Session(engine)

    summary = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()

    session.close() 


    summary_list = []

    #for i in range(len(summary)):
    #    summary_list.append(summary[i])

    return jsonify(summary)



if __name__ == "__main__":
    app.run(debug=True)
