<a href="http://orangered.io">orangered.io</a>

## development

To run the app locally (might remove this since minikube does everything now):

    make db
    make run-dev

### Minikube instructions

Start minikube and enable ingress addon:

    minikube start
    minikube addons enable ingress

Build local image:

    eval $(minikube docker-env)
    docker build -t orangered .

Run:

    kubectl create -f kubernetes/minikube/

To apply changes to the container, build it again (`docker build` step) then delete the running pod using `kubectl`.

Create the database:

    kubectl exec -it <postgres pod name> -- createdb -U orangered_user orangered

Create the database tables and base data:

    kubectl exec -it <orangered pod name> -- python -c 'from app import db; db.create_all()'
    kubectl exec -it <orangered pod name> -- python -c 'from utils import insert_subreddits; insert_subreddits()'

Modify hosts file to point to the minikube ingress:

    echo "$(minikube ip) dev.orangered.io" | sudo tee -a /etc/hosts

Go to <a href="http://dev.orangered.io">dev.orangered.io</a> to see your sweet new running app.


### Google cloud instructions:

Install gcloud tooling and set up authentication.

To create cluster:

    gcloud container clusters create orangered \
        --num-nodes 2 \
        --zone us-east4-a \
        --enable-ip-alias \
        --cluster-version 1.12.7-gke.10

To resize the cluster node pool:

    gcloud container node-pools create small-pool \
        --cluster orangered \
        --zone us-east4-a \
        --num-nodes 1 \
        --machine-type g1-small \
        --disk-size 10GB

    # cordon all old nodes (run for each old node)
    kubectl cordon <default-pool node name>

    # drain all old nodes (run for each old node)
    kubectl drain \
        --force \
        --ignore-daemonsets \
        --delete-local-data \
        --grace-period=10 \
        <default-pool node name>

    gcloud container node-pools delete default-pool \
        --cluster orangered \
        --zone us-east4-a

To build container:

    docker build -t gcr.io/orangered/orangered .

Push container:

    docker push gcr.io/orangered/orangered

Add secrets (fill in values before running commands):

    kubectl create secret generic psql-creds \
        --from-literal=pgdatabase= \
        -–from-literal=pghost= \
        --from-literal=pguser= \
        --from-literal=pgpassword=

    kubectl create secret generic mailgun-creds \
        --from-literal=mailgun-api-key=

    kubectl create secret generic reddit-creds \
        --from-literal=reddit-client-id= \
        --from-literal=reddit-client-secret= \
        --from-literal=reddit-username= \
        --from-literal=reddit-password=

    kubectl create secret generic recaptcha \
        --from-literal=recaptcha-site-key= \
        --from-literal=recaptcha-secret-key=

Deploy orangered:

    kubectl create -f kubernetes/gke/

To rebuild and deploy the container, run the `docker build` and `docker push` steps again, then delete the pods.

Create the database tables and base data:

    kubectl exec -it <orangered pod name> -- python -c 'from app import db; db.create_all()'
    kubectl exec -it <orangered pod name> -- python -c 'from utils import insert_subreddits; insert_subreddits()'

To scale, simply:

    kubectl scale deployment orangered --replicas=2


### Database notes

In production, a Postgres 11 database is running in Google Cloud SQL with a private IP, username, and password created in the console and stored as kubernetes secrets in the production cluster.

To access via `psql` run:

    kubectl exec -it <postgres pod name> -- psql


### Reddit client notes


### Mailgun notes

