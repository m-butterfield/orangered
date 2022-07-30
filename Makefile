cloudrunbasecommand := gcloud run deploy --project=mattbutterfield --region=us-central1 --platform=managed
deployservercommand := $(cloudrunbasecommand) --image=gcr.io/mattbutterfield/mattbutterfield.com mattbutterfield
deployworkercommand := $(cloudrunbasecommand) --image=gcr.io/mattbutterfield/mattbutterfield.com-worker mattbutterfield-worker

terraformbasecommand := cd infra && terraform
terraformvarsarg := -var-file=secrets.tfvars

export PGHOST=localhost
export PGDATABASE=orangered

deploy: docker-build docker-push
	$(deployservercommand)
	$(deployworkercommand)

deploy-server: docker-build-server docker-push-server
	$(deployservercommand)

deploy-worker: docker-build-worker docker-push-worker
	$(deployworkercommand)

docker-build:
	docker-compose build

docker-build-server:
	docker-compose build server

docker-build-worker:
	docker-compose build worker

docker-push:
	docker-compose push

docker-push-server:
	docker-compose push server

docker-push-worker:
	docker-compose push worker

reset-db:
	dropdb --if-exists orangered
	createdb orangered
	python -c 'from app import db; db.create_all()'
	python -c 'from utils import insert_subreddits; insert_subreddits()'

migrate:
	go run cmd/migrate/main.go

fmt:
	black .
	cd infra/ && terraform fmt

run-server: export FLASK_APP=app.py
run-server: export FLASK_DEBUG=1
run-server:
	flask run -p 8000

run-worker: export FLASK_APP=worker.py
run-worker: export FLASK_DEBUG=1
run-worker:
	flask run -p 8001

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
	cd infra && terraform init -upgrade && cd -
