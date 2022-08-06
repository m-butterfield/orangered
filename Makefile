cloudrunbasecommand := gcloud run deploy --project=mattbutterfield --region=us-central1 --platform=managed
deployservercommand := $(cloudrunbasecommand) --image=gcr.io/mattbutterfield/orangered.email orangered

terraformbasecommand := cd infra && terraform
terraformvarsarg := -var-file=secrets.tfvars

export PGHOST=localhost
export PGDATABASE=orangered
export FLASK_DEBUG=1

deploy: docker-build docker-push
	$(deployservercommand)

deploy-server: docker-build docker-push
	$(deployservercommand)

docker-build:
	docker-compose build

docker-push:
	docker-compose push

reset-db:
	dropdb --if-exists orangered
	createdb orangered
	python -c 'from app import db; db.create_all()'
	python -c 'from utils import insert_subreddits; insert_subreddits()'

fmt:
	black .
	yarn run eslint static/ts/ --fix
	cd infra/ && terraform fmt

run-server: export FLASK_APP=app.py
run-server:
	flask run -p 8000

run-webpack:
	yarn run webpack --mode development --watch

send-test-emails: export SERVER_NAME=localhost
send-test-emails:
	./send_emails

test: export SERVER_NAME=orangered.email
test: export PGDATABASE=orangered_test
test:
	dropdb --if-exists orangered_test
	createdb orangered_test
	python -m unittest -v $(filter-out $@,$(MAKECMDGOALS))

tf-plan:
	$(terraformbasecommand) plan $(terraformvarsarg)

tf-apply:
	$(terraformbasecommand) apply $(terraformvarsarg)

tf-refresh:
	$(terraformbasecommand) apply $(terraformvarsarg) -refresh-only

update-deps:
	poetry update
	yarn upgrade
	cd infra && terraform init -upgrade && cd -
