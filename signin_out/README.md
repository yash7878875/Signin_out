Create a virtual environment (optional but recommended):

windows-> python -m venv venv
mac -> source venv/bin/activate

Install the required packages:

-> pip install -r requirements.txt

Apply makemigrations to set up the database:

-> python manage.py makemigrations

Apply migrate to set up the database:

-> python manage.py migrate

Run the development server:

-> python manage.py runserver

Access the API endpoints at http://127.0.0.1:8000/register/.
