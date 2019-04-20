db:
	python -c 'from app import db; db.create_all()'
	sqlite3 app.db < insert_subreddits.sql
