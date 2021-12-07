# Old-Stuff
**https://github.com/Auction-Wariors/old-stuff**
### How to run:

Old-Stuff is written and tested in Python > 3.9.5.  
Although it will probably run on older Python we recommend running on
3.9.5 or newer.

Steps to get old-stuff up and running:

* Unzip to a suitable location on your computer.
* Open a terminal in the unzipped folder
* create a python virtual environment
````
> python3 -m venv venv
````
* activate the virtual environment 
````
> /venv/Scripts/activate.ps1
# or
> /venv/Scripts/activate.bat
````
If you are on unix systems
````
> source venv/bin/activate
````
* install python decencies to the virtual environment
````
(venv) > pip3 install -r rewuirements.txt
````
* Navigate to the app folder
````
(venv) > cd app
````
* Create DB migrations and create DB
````
(venv) app/> python3 manage.py makemigrations
(venv) app/> python3 manage.py migrate
````
* Seed DB with initial data
````
(venv) app/> python3 manage.py populate
````
* Run development server
````
(venv) app/> python3 manage.py runserver
````

### How to test:
#### Running tests

In the main/app folder containing the 'manage.py' run:
(remember to activate virtual environment!)
````
(venv) app/> python3 manage.py test
````
---
#### Running coverage and building a HTML coverage report
In the main/app folder containing the 'manage.py' run:
(remember to activate virtual environment!)
````
(venv) app/> coverage run --source='.' manage.py test
(venv) app/> coverage html
````
To view the coverage report open `app/htmlcov/index.html`
