
#!/bin/bash
docker run --rm -v $(pwd)/app:/app rasa/rasa:latest train --domain /app/domain.yml --data /app/data/ --out /app/models
docker build -t rasa:local -f Dockerfile-rasa .
docker build -t rasa-action-server:local -f Dockerfile-rasa-action-server .
docker build -t rasa-frontend:local -f Dockerfile-frontend .

echo 'Check your models/ folder periodically and delete out old models. This demo will not clean up for you.'