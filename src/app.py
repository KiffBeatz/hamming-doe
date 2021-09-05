from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
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

   labels = [row[0] for row in data]
   values = [row[1] for row in data]

   return render_template("graph.html", labels=labels, values=values)


if __name__ == '__main__':
   app.run()
