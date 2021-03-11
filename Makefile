images:
	docker build -t arteia-api-image -f api.Dockerfile .
	docker build -t arteia-worker-image -f worker.Dockerfile .
