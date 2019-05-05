<a href="https://orangered.io">orangered.io</a>

## development

To run the app locally:

    make db
    make run-dev


required environment variables:

    MAILGUN_API_KEY
    REDDIT_CLIENT_ID  
    REDDIT_CLIENT_SECRET  
    REDDIT_USERNAME  
    REDDIT_PASSWORD  
    SQLALCHEMY_DATABASE_URI


### Minikube instructions

Start minikube and enable ingress addon:

    minikube start
    minikube addons enable ingress

Build local image:

    eval $(minikube docker-env)
    docker build -t orangered .

Run:

    kubectl create -f kubernetes/local/

To apply changes to the container, build it again (`docker build` step) then delete the running pod using `kubectl`.

Create the database:

    kubectl exec -it <postgres pod name> -- createdb -U orangered_user orangered

Create the database tables and base data:

    kubectl exec -it <orangered pod name> -- python -c 'from app import db; db.create_all()' && python -c 'from subreddits import insert_subreddits; insert_subreddits()'

Modify hosts file to point to the minikube ingress:

    echo "$(minikube ip) dev.orangered.io" | sudo tee -a /etc/hosts

Go to <a href="dev.orangered.io">dev.orangered.io</a> to see your sweet new running app.

To scale, simply:

    kubectl scale deployment orangered --replicas=2


### Google cloud instructions:

Install gcloud tooling and set up authentication.

To create cluster:

    gcloud container clusters create orangered \
        --scopes "cloud-platform" \
        --num-nodes 2 \
        --enable-basic-auth \
        --issue-client-certificate \
        --enable-ip-alias \
        --zone us-east4

To build container:

    docker build -t gcr.io/orangered/orangered .

Push container:

    docker push gcr.io/orangered/orangered

Deploy orangered:

    kubectl create -f kubernetes/remote/

To rebuild and deploy the container, run the `docker build` and `docker push` steps again, then delete the pods.

