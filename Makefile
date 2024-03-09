IMAGE_NAME=acct-mamt-image
CONTAINER_NAME=acct-mamt-app

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop and remove the Docker container
stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

# Remove the Docker image
remove-image:
	docker rmi $(IMAGE_NAME)

# Stop and remove the container, and remove the image
clean: stop remove-image

.PHONY: build run stop remove-image clean
