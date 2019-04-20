db:
	python -c 'from app import db; db.create_all()'
	sqlite3 app.db < insert_subreddits.sql

run-dev:
	FLASK_APP=app.py FLASK_DEBUG=1 flask run

test:
	SQLALCHEMY_DATABASE_URI='sqlite:///test.db' python -c 'from app import db; db.create_all()'
	sqlite3 test.db < insert_subreddits.sql
	SQLALCHEMY_DATABASE_URI='sqlite:///test.db' python -m unittest -v tests
	rm test.db
