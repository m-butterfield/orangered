<a href="https://orangered.io">orangered.io</a>

## development

To run the app locally:

    $ make db
    $ make run-dev


required environment variables:

    MAILGUN_API_KEY
    REDDIT_CLIENT_ID  
    REDDIT_CLIENT_SECRET  
    REDDIT_USERNAME  
    REDDIT_PASSWORD  
    SQLALCHEMY_DATABASE_URI


### Minikube instructions

Start minikube:

    $ minikube start

Build local image:

    $ eval $(minikube docker-env)
    $ docker build -t orangered .

Run:

    $ kubectl apply -f kubernetes/local

Run this same command to apply changes to all or specific yaml files.

To delete the deployment run:

    $ kubectl delete deployment (name of deployment)

To apply changes to the container, build it again (`docker build` step) then delete the running pod using `kubectl`.


### Google cloud instructions:

Install gcloud tooling and set up authentication.

To create cluster:

    $ gcloud container clusters create orangered \
          --scopes "cloud-platform" \
          --num-nodes 2 \
          --enable-basic-auth \
          --issue-client-certificate \
          --enable-ip-alias \
          --zone us-east4

To build container:

    $ docker build -t gcr.io/orangered/orangered .

Push container:

    $ docker -- push gcr.io/orangered/orangered


Deploy orangered:

    $ 
