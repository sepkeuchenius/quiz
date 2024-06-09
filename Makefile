build:
	docker build . -t sep/quiz:develop --platform linux/amd64

run:
	docker run sep/quiz:develop

develop:
	fastapi dev main.py

yeet: build
	docker tag sep/quiz:develop europe-west4-docker.pkg.dev/reuniquiz/prod/app:prod
	docker push europe-west4-docker.pkg.dev/reuniquiz/prod/app:prod

gcloud-init:
	gcloud init

gcloud-auth:
	gcloud auth configure-docker europe-west4-docker.pkg.dev

deploy:
	gcloud run services replace gcloud/service.yaml