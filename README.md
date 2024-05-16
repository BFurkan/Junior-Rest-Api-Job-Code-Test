#Junior Dev Assignment
Features
Create new students with their names, surnames, student numbers, and corresponding grades.
Store student data in a database.
Calculate the average grade for each course.
Installation
To run the API locally, follow these steps:

Clone this repository
Navigate to the project directory
Install the required dependencies

  pip install flask
  pip install flask_sqlalchemy
  
Run the Flask application
  python run.py
  
The API should now be accessible at http://localhost:5000.

Test Case on Postman

  {
  "name": "Arthur",
  "surname": "Brown",
  "std_number": "34578",
  "grades": [
    {
      "code": "MT101",
      "value": 95
    },
    {
      "code": "HS101",
      "value": 90
    }
  ]
}


