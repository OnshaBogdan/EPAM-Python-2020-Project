# EPAM-Python-2020-Project    
 [![Build Status](https://travis-ci.org/OnshaBogdan/EPAM-Python-2020-Project.svg?branch=main)](https://travis-ci.org/OnshaBogdan/EPAM-Python-2020-Project) [![Coverage Status](https://coveralls.io/repos/github/OnshaBogdan/EPAM-Python-2020-Project/badge.svg?branch=main)](https://coveralls.io/github/OnshaBogdan/EPAM-Python-2020-Project?branch=main)    
  
  
# Description  
EmployeeManagement - simple tool for managing Employees and their Departments using GUI or RESTful API.  
  
# Installation     
## Prerequisites 
Make sure you have installed all of the following prerequisites on your development machine:  
- Python 3.6+ (with `setuptools`,  `wheel` and `virtualenv` packages)  
  
## Install and configure MySQL: 
- Install mysql client and required packages:    
```bash 
sudo apt update 
sudo apt-get install python3.6-dev -y 
sudo apt-get install libsqlclient-dev -y 
sudo apt-get install libmysqlclient-dev -y 
sudo apt-get install libssl-dev -y 
sudo apt-get install mysql-client -y 
``` 
- Install mysql server:    
```bash 
sudo apt install mysql-server -y  
```    
 - Create mysql user:
```bash 
sudo mysql -e "CREATE USER 'djangouser'@'localhost' IDENTIFIED BY 'password';" 
```
- Grant all privileges on database to the user:    
```bash 
sudo mysql -e "GRANT ALL PRIVILEGES ON * . * TO 'djangouser'@'localhost';" 
```    
## Set up project: 
 - Clone repository:     
  
```bash  
git clone https://github.com/OnshaBogdan/EPAM-Python-2020-Project  
```    
 - Move into project root folder:    
 ```bash 
 cd EPAM-Python-2020-Project/ 
 ```
 
 - Create virtual environment:    
```bash  
virtualenv -p python .venv  
```  
  - Activate virtual environment:    
```bash  
. .venv/bin/activate  
```  
  - Move into django project:    
```bash  
cd employee_management/  
``` 
- Install dependencies:    
```bash  
python -m pip install -r requirements.txt  
```  
  
- Prepare database:    
```bash  
python manage.py makemigrations
python manage.py migrate  
```  
  - Set environment variables:   
```bash  
export DB_USER=djangouser  
export DB_NAME=employee_management  
export DB_PASSWORD=password  
export SECRET_KEY=YOUR_SECRET_KEY  
```  
 - Prepare static files:    
```bash
python manage.py collectstatic
```  
  - [Optional] Create superuser:    
```bash 
python manage.py createsuperuser
```    
## Run  
- Development server:  
```bash
python manage.py runserver 80
```  
Web app will be available locally [here](http://127.0.0.1/).  
  
- Production server:  
```bash 
gunicorn employee_management.wsgi --bind 0.0.0.0:80
```  
Web app will be available:
- Locally - `http://127.0.0.1/`
- Globally - `http://{PUBLIC_IP}/` (you must have proper inbound rules set).   
 
API root can be accessed at `/api` subdirectory.
  
## Tests:  
To check tests, run:  
```bash  
python manage.py test  
```  
All tests are stored in  [department_app/tests.py](employee_management/department_app/tests.py)  
  
## Code Coverage  
To check code coverage, run:  
```bash  
coverage erase  
coverage run  
coverage report  
```  
You can edit coverage settings in [.coveragerc](employee_management/.coveragerc)