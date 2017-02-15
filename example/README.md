##Example Project for support_tickets

This example is provided as a convenience feature to allow potential users to try the app straight from the app repo without having to create a django project.

It can also be used to develop the app in place.

To run this example, follow these instructions:

1. Clone the repository
		$ git clone git://github.com/bazzite/django-support-tickets.git

2. Navigate to the `example` directory


3. Creat a virtual environment
		$ virtualenv venv
		$ . venv/bin/activate

4. Install the requirements for the package:
		
		pip install -r requirements.txt
		
5. Make and apply migrations

		python manage.py makemigrations
		
		python manage.py migrate
		
6. Run the server

		python manage.py runserver
		
7. Access from the browser at `http://127.0.0.1:8000`
