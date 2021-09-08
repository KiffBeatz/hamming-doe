from sqlalchemy.sql.expression import label
from database_model import db, Data

def initialize_database():
    db.drop_all()
    db.create_all()

def set_data(data_array : list):
    for var in data_array:
        _add_data(var)

    db.session.commit()
def _add_data(v1):
    var = Data(date = v1[0], values = v1[1])

    db.session.add(var)

def get_data():
    print(type(Data.query.all()))
    return Data.query.all()

def get_all_dates():
    label = [dates.date for dates in Data.query.all()]
    return label

def get_all_values():
    values = [dates.values for dates in Data.query.all()]
    return values