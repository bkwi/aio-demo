### local setup
* `make images`
* `docker-compose up`

Run with multiple workers:
```sh
docker-compose up --scale arteia-worker=3
```

Run 25 requests:
```
docker exec arteia-api-container python schedule_multiple.py --num-requests 25
```
