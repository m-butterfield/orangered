cloudrunbasecommand := gcloud run deploy --project=mattbutterfield --region=us-central1 --platform=managed
deployservercommand := $(cloudrunbasecommand) --image=gcr.io/mattbutterfield/orangered.email orangered

terraformbasecommand := cd infra && terraform
terraformvarsarg := -var-file=secrets.tfvars

export PGHOST=localhost
export PGDATABASE=orangered
export FLASK_DEBUG=1

.PHONY: deploy deploy-server docker-build docker-push reset-db fmt run-server run-webpack run-webpack-prod update-static send-test-emails scrape-subreddits test mypy tf-plan tf-apply tf-refresh update-deps

deploy: docker-build docker-push
	$(deployservercommand)

deploy-server: docker-build docker-push
	$(deployservercommand)

docker-build: run-webpack-prod
	docker-compose build

docker-push:
	docker-compose push

reset-db:
	dropdb --if-exists orangered
	createdb orangered
	python -c 'from db import Base, engine; Base.metadata.create_all(engine)'
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

run-webpack-prod:
	rm -rf static/js/dist
	yarn run webpack --mode production

update-static:
	rm -rf _site
	mkdir _site
	./update_static
	mkdir -p _site/static/js/dist/
	cp static/js/dist/* _site/static/js/dist

send-test-emails: export SERVER_NAME=localhost
send-test-emails:
	./send_emails

scrape-subreddits:
	./scrape_subreddits

test: export SERVER_NAME=orangered.email
test: export PGDATABASE=orangered_test
test:
	dropdb --if-exists orangered_test
	createdb orangered_test
	python -m unittest -v $(filter-out $@,$(MAKECMDGOALS))

mypy:
	mypy . --strict

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
