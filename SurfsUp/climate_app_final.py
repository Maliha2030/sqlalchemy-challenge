    #########################################################################
##                                                                     ##
##   0. Imports                                                        ##
##                                                                     ##
#########################################################################

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect

from flask import Flask, jsonify


#########################################################################
##                                                                     ##
##   Starting DB
##                                                                     ##
#########################################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
# mapped classes are now created with names by default matching that of the table name.
measurement = Base.classes.measurement
Station = Base.classes.station

##################################################
# Flask Setup
##################################################
app = Flask(__name__)

#################################################
# Flask Route
#################################################

##define different app routes & what we do everytime reach that route
##associate an end point or url with the result of a function call
##start at homepage list all available routes

@app.route("/")

def home():

    print("define app routes")
    return (

       f"Precipitation Data for One Year: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Active Weather Stations: <br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations of the Most-Active Station for One Year: <br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"The Average, Maximum, and Minimum Temperature for a specified Start Date(yyyy-mm-dd for example 2017-08-16) :<br/>"
        f"/api/v1.0/start<br/>"
        f"<br/>"
        f"The Average, Maximum, and Minimum Temperatures for a specified Start and End Date(yyyy-mm-dd/yyyy-mm-dd):<br/>"
        f"/api/v1.0/start/end"
    )

##convert query results from precipitation analysis retrieve only the last 12 months of data to a dictionary using date as the key and prcp as the value.
##Return the JSON representation of your dictionary.


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set
    date_year_ago = dt.date(2017,8,23) - dt.timedelta(days=1*365)  
    
    # Query to retrieve data and precipitation scores
    precip_scores=session.query(measurement.date, measurement.prcp).filter(measurement.date>=date_year_ago)
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary from the row data and append to a list of prcp_data. Use "date" as the key and "prcp" as the value.
    # Dictionary to be converted into json response. 
    prcp_data = []
    for date, prcp in precip_scores:
        prcp_data_dict = {}
        prcp_data_dict["date"] = prcp
        prcp_data.append(prcp_data_dict)
        
    return jsonify(prcp_data)


@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate date one year from the last date in data set
    date_year_ago = dt.date(2017,8,23) - dt.timedelta(days=1*365)  
    
    # Query dates and temperature observations of the most active station for the previous year of data
    active_stations = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
                            filter(measurement.date >= date_year_ago).all()
    
    
    # Close Session                                                  
    session.close()
    
    # Create a dictionary from the row data and append to list most_active
    most_active = []
    for date, temp in active_stations:
        active_dict = {}
        active_dict[date] = temp
        most_active.append(active_dict)
        
    return jsonify(most_active)
        
     
if __name__ == '__main__':
    app.run(debug=True)

    