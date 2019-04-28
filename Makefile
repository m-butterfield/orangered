db:
	@createdb orangered
	@python -c 'from application import db; db.create_all()'
	@python -c 'from subreddits import insert_subreddits; insert_subreddits()'

run-dev:
	FLASK_APP=application.py FLASK_DEBUG=1 flask run

test:
	@dropdb --if-exists orangered_test
	@createdb orangered_test
	SQLALCHEMY_DATABASE_URI='postgresql://localhost/orangered_test' python -m unittest -v $(filter-out $@,$(MAKECMDGOALS))
