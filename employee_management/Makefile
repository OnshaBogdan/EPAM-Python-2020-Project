.PHONY : install_mysql install run_dev run_prod test

install:
	make install_mysql
	pip install -r requirements.txt
	python manage.py makemigrations --no-input
	python manage.py migrate --no-input

install_mysql:
	apt update
	apt-get install python3.6-dev -y
	apt-get install libsqlclient-dev -y
	apt-get install libmysqlclient-dev -y
	apt-get install libssl-dev -y
	apt-get install mysql-client -y

run_dev:
	python manage.py runserver 8000

run_prod:
	gunicorn employee_management.wsgi --bind 0.0.0.0:80

test:
	coverage erase
	coverage run manage.py test
	coverage report
