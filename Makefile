db:
	@createdb orangered
	@python -c 'from app import db; db.create_all()'
	@python -c 'from utils import insert_subreddits; insert_subreddits()'

run-dev:
	FLASK_APP=app.py FLASK_DEBUG=1 flask run

test:
	@dropdb --if-exists orangered_test
	@createdb orangered_test
	PGHOST='localhost' PGDATABASE='orangered_test' python -m unittest -v $(filter-out $@,$(MAKECMDGOALS))
