

# Python SQL toolkit and Object Relational Mapper

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, inspect

from flask import Flask, jsonify

import datetime as date

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Database = automap_base()

# reflect the tables
Database.prepare(engine, reflect=True)

# View all of the classes that automap found
Database.classes.keys()

# Save references to each table 
Measurement = Database.classes.measurement
Station = Database.classes.station

# Session (link) from Python to the Database
session = Session(bind=engine)
inspector = inspect(engine)

app = Flask(__name__)

@app.route("/")
def homepage():
	#List all routes that are available in the home page
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(bind=engine)
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last12months = (date.datetime.strptime(recent_date[0], '%Y-%m-%d') - date.timedelta(days=365)).date()
    last12months_prec_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last12months ).\
    order_by(Measurement.date).all()
    #Convert the query results to a Dictionary using date as the key and prcp as the value.
    prcp_totals = []
    for result in last12months_prec_data:
        row = {}
        row["date"] = result[0]
        row["prcp"] = result[1]
        prcp_totals.append(row)
    #Return the JSON representation of your dictionary.
    return jsonify(prcp_totals)

@app.route("/api/v1.0/stations")
def station():
	#query to get the stations.
	station_query = session.query(Station.name, Station.station)
	stations = pd.read_sql(station_query.statement, station_query.session.bind)
	return jsonify(stations.to_dict())

if __name__=="__main__":
    app.run(debug=True)