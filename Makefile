
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_FILE = -f docker-compose.yml
BUILD = $(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) build
UP = $(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) up
DOWN = $(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) down
RESTART = $(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) restart
LOGS = $(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) logs

# Default target to build and run the services
all: build up

# Build the services
build:
	$(BUILD)

# Start the services in the background
up:
	$(UP)

# Bring down the services
down:
	$(DOWN)

# Restart the services
restart:
	$(RESTART)

# View logs for all services
logs:
	$(LOGS)

# Stop the services (without removing volumes)
stop:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) stop

# Clean up the services and remove volumes
clean:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) down -v

#copy the user_data from the container
copy:
	docker cp 42hackathon_rspb-backend-1:app/data/user_data.json .
