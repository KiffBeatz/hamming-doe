# hamming-doe
A dynamic design of experiment (DOE) that statistically analyzes a set of experiment data, using neural networks (NN), in order to find how the input features effects the outputs of the experimentation. Specifically, finding which input features can optimize the output in order to reduce the overall need of extensive experimentation.

"requirements.txt." is for the libraries needed to run the web app.
Install a python virtual environment, then activate the environment
and then install all the libraries using 'pip install -r requirements.txt'

INSTRUCTIONS TO RUN:
cd doe
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

TO VIEW ADMIN PORTAL:
cd doe
python manage.py createsuperuser

then just enter admin for username, admin@admin.com for email, and then admin for password
So you can view tables and users at http://127.0.0.1:8000/admin/
