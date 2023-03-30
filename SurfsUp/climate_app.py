    #########################################################################
##                                                                     ##
##   0. Imports                                                        ##
##                                                                     ##
#########################################################################
# 0.1 Import Flask, jsonify ,SQLAlchemy

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

engine = create_engine("sqlite:/hawaii.sqlite")

# reflect an existing database into a new model
# reflect the tables
Base = automap_base()

Base.prepare(autoload_with=engine)

# Save references to each table
# mapped classes are now created with names by default
# matching that of the table name.
measurement = Base.classes.measurement
Station = Base.classes.station

##################################################
# Flask Setup
##################################################
app = Flask(__name__)

##################################################
# Flask Route
##################################################

@app.route("/")


if __name__ == '__main__':
    app.run(debug=True)