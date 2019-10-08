#!/bin/sh

# Deploy the stack if it hasn't been deployed yet
docker stack deploy -c docker-compose.yml --prune rasa-wc-example

# Force latest images to the deployment -- required if not using a registry
docker service update rasa-wc-example_action-server --image rasa-action-server:local --force 
docker service update rasa-wc-example_rasa --image rasa:local --force
docker service update rasa-wc-example_frontend --image rasa-frontend:local --force