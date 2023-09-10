# AI-generated Subtitles - Web Application by Margot Berton

Last update: 08/25/2023
NB: The application uses several Google APIs and is deployed on a Google VM. All these services depend on a free trial to Google Cloud, which will end on October 30, 2023.


## Dependencies and Requirements

* Some dependencies are required; refer to requirements.txt if needed.
* To use the application with your Google Project ID, you will need the following permissions:
	- Cloud Speech Administrator
	- Cloud Translation API Administrator
	- Cloud Infrastructure Manager Admin
	- Storage Administrator
  and the following APIs:
  	- Cloud Speech-to-Text API
  	- Cloud Translation API
  	- Cloud Resource Manager API
  	- Cloud Storage API
  Otherwise: use the default entered Google Project ID (available by October 30, 2023).


## Running the Application

1. Navigate to the project directory: cd <path-to-subtitling-app>/subtitling-app
2. Launch the Django application: python manage.py runserver

OR

1. Go to the URL http://34.16.168.10/ (available by October 30, 2023).
