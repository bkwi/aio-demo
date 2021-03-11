### local setup
* `make images`
* `docker-compose up`

Run 25 requests:
```
docker exec arteia-api-container python schedule_multiple.py --num-requests 25
```
