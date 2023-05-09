run_db:
	docker-compose run -d --rm --publish 54322:5432 db

clean_db:
	docker-compose stop
	sudo rm -rf pgdata
	mkdir pgdata