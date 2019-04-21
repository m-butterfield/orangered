db:
	createdb orangered
	python -c 'from application import db; db.create_all()'
	psql -d orangered -f insert_subreddits.sql

run-dev:
	FLASK_APP=application.py FLASK_DEBUG=1 flask run

test:
	dropdb --if-exists orangered_test
	createdb orangered_test
	SQLALCHEMY_DATABASE_URI='postgresql://localhost/orangered_test' python -c 'from application import db; db.create_all()'
	psql -d orangered_test -f insert_subreddits.sql
	SQLALCHEMY_DATABASE_URI='postgresql://localhost/orangered_test' python -m unittest -v tests
