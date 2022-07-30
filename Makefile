cloudrunbasecommand := gcloud run deploy --project=mattbutterfield --region=us-central1 --platform=managed
deployservercommand := $(cloudrunbasecommand) --image=gcr.io/mattbutterfield/orangered.email orangered
deployworkercommand := $(cloudrunbasecommand) --image=gcr.io/mattbutterfield/orangered.email orangered-worker

terraformbasecommand := cd infra && terraform
terraformvarsarg := -var-file=secrets.tfvars

export PGHOST=localhost
export PGDATABASE=orangered

deploy: docker-build docker-push
	$(deployservercommand)
	$(deployworkercommand)

deploy-server: docker-build docker-push
	$(deployservercommand)

deploy-worker: docker-build docker-push
	$(deployworkercommand)

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
