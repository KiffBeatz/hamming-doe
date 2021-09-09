from flask import Flask, render_template
from database_model import app
from database_api import initialize_database, set_data, get_all_dates, get_all_values, get_data, get_values_below_a_thousand

@app.route('/')
def home():
   initialize_database()
   # irrelevant test data
   data = [
      ("01-01-2021", 1597),
      ("02-01-2021", 1456),
      ("03-01-2021", 1908),
      ("04-01-2021", 896),
      ("05-01-2021", 755),
      ("06-01-2021", 453),
      ("07-01-2021", 1100),
      ("08-01-2021", 1234),
      ("09-01-2021", 1478),
   ]

   set_data(data)

   labels = get_all_dates()
   values = get_all_values()

   print(get_data()[0].date)
   print(get_values_below_a_thousand())

   return render_template("graph.html", labels=labels, values=values)


if __name__ == '__main__':
   app.run()
