DC = docker compose
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
DB_CONTAINER = postgres-db
ENV_FILE = --env-file .env
APP_CONTAINER = car-factory-app
LOGS = docker logs


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV_FILE} up -d --remove-orphans

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f
