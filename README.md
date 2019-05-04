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


Google cloud instructions:

Install gcloud tooling and set up authentication.

To create cluster:

    $ 


To build container:

    $ docker build -t gcr.io/orangered/orangered .

Push container:

    $ gcloud docker -- push gcr.io/orangered/orangered
