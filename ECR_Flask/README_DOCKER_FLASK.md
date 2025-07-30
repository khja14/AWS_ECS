# How to Build and Run the Flask App with Docker

## 1. Build the Docker image

Open a terminal in the `ECR` directory and run:

```
docker build -t flask-hello-app .
```

## 2. Run the Docker container and connect from the host machine

To allow access from your host machine (e.g., http://127.0.0.1:5000), run:

```
docker run --rm -p 5000:5000 flask-hello-app
```

- This command maps the container's port 5000 to your host's port 5000.
- Access the Flask app at: http://127.0.0.1:5000

## 3. Stop the container

Press `Ctrl+C` in the terminal, or find the container ID with:

```
docker ps
```

Then stop it with:

```
docker stop <container_id>
```

---
**Note:**  
- If you change the code, rebuild the image with the build command above.
- The app will respond with "Hello, World!" at the root URL.
- The `--rm` option automatically removes the container after it stops.