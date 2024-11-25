# Bird Identification Chatbot

An AI based chatbot application that helps users identify birds based on matching descriptions. The system provides percentage-based matching to help users accurately identify bird species.

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose
- Make (typically pre-installed on Unix-based systems)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/emgervais/42Hackathon_RSPB.git
cd 42Hackathon_RSPB
```

2. Build and start the services:
```bash
make
```

## Usage

The project uses a Makefile to simplify Docker operations. Here are the available commands:

### Basic Commands

- `make all`: Build and start all services (default command)
- `make build`: Build the Docker services
- `make up`: Start the Docker services
- `make down`: Stop and remove the Docker services
- `make stop`: Stop the services without removing containers
- `make restart`: Restart all services
- `make logs`: View logs from all services
- `make clean`: Stop services and remove containers, networks, and volumes
- `make copy`: Copy user data from the container to your local machine

### Example Usage

To start the application for the first time:
```bash
make all
```

To view the application logs:
```bash
make logs
```

## Docker Services

The application runs in Docker containers managed by Docker Compose. The services include:
- Backend service
- Frontend services

## Data Management

User data is stored within the Docker container and can be extracted using:
```bash
make copy
```
This will copy the user_data.json file from the container to your local directory.
