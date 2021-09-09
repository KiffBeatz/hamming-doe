from sqlalchemy.sql.expression import label
from database_model import db, Data

#Clears out and set up database
def initialize_database():
    db.drop_all()
    db.create_all()

#Takes an array of data and feeds it into database
def set_data(data_array : list):
    for var in data_array:
        _add_data(var)
    db.session.commit()

#Adds data piece by piece
def _add_data(v1):
    var = Data(date = v1[0], values = v1[1])
    db.session.add(var)

#Returns all data in database
def get_data():
    return Data.query.all()

#Returns all dates in data
def get_all_dates():
    label = [dates.date for dates in Data.query.all()]
    return label

#Returns all values in data
def get_all_values():
    values = [dates.values for dates in Data.query.all()]
    return values

#Returns all data with values below a thousand
def get_values_below_a_thousand():
    values = Data.query.filter(Data.values < 1000)
    return values

#Returns all data with values above a thousand
def get_values_above_a_thousand():
    values = Data.query.filter(Data.values > 1000)
    return values