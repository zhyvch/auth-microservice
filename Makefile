DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
AUTH_SERVICE_FILE = docker_compose/auth-service.yaml
AUTH_SERVICE_STORAGE_FILE = docker_compose/auth-service-storages.yaml
ENV = --env-file .env
AUTH_SERVICE_CONTAINER = auth-service

.PHONY: auth-service-storages
auth-service-storages:
	${DC} -f ${AUTH_SERVICE_STORAGE_FILE} ${ENV} up --build -d

.PHONY: auth-service-storages-down
auth-service-storages-down:
	${DC} -f ${AUTH_SERVICE_STORAGE_FILE} down

.PHONY: auth-service-storages-logs
auth-service-storages-logs:
	${LOGS} ${AUTH_SERVICE_CONTAINER} -f

.PHONY: auth-service
auth-service:
	${DC} -f ${AUTH_SERVICE_FILE} ${ENV} up --build -d

.PHONY: auth-service-down
auth-service-down:
	${DC} -f ${AUTH_SERVICE_FILE} down

.PHONY: auth-service-logs
auth-service-logs:
	${LOGS} ${AUTH_SERVICE_CONTAINER} -f

.PHONY: all
all:
	${DC} -f ${AUTH_SERVICE_STORAGE_FILE} -f ${AUTH_SERVICE_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${AUTH_SERVICE_STORAGE_FILE} -f ${AUTH_SERVICE_FILE} down

