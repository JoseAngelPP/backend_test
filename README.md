# Backend test

## Set up
### Build DRF app and celery

`make build-app`

`make build-worker`

### Start project
`make up`

### (Optional) Stop Celery
Celery is used to asyn task to send emails, we can stop it

`make stop-celery`

### Run tests

`make tests`