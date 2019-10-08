# WORK IN PROGRESS

# rasa-webchat-docker-stack-example
A fully functional Rasa-based webchat bot using Docker Stack for easy deployment.


# Requirements

You need the following installed and ready:
* Docker
* Linux, macOS, or some form of a bash-like shell on Windows
* Port 8042 open/unused -- adjust in docker-compose.yml under the traefik section if needed

For editing I use VSCode, but you are welcome to use whatever you are comfortable with.


# Setup

If you have not set your Docker to Swarm mode, do by issuing `docker swarm init`. Swarm mode is designed to make it easy to link up multiple Docker nodes together, but this is not needed here (so ignore the join key information). We're just going to leverage the Swarm Mode features. Single node works just fine.

# Building

Run the `./build.sh` script to generate the Docker images for Rasa and its Action Server.


# Running

1. Run `./deploy.sh` to deploy your built images.
2. Access the webchat interface at http://localhost:8042/


# Editing / Customizing

1. Read the Rasa docs to familiarize yourself with the system and how it works: https://rasa.com/docs
2. Edit `domain.yml` to reflect any new slots, intents, messages, etc.
3. Edit `app/actions/actions.py` to customize action response routines or add new ones
4. Edit `data/nlu.md` to add new training data for intent mapping (e.g., understanding what a user is trying to say and extracting any keywords)
5. Edit `data/stories.md` to add new training data for conversation path mapping (e.g., what set of responses or actions the bot should take in response to a type of request from a user)
6. When you've edited the file(s) you need to, simply run the Build and Deploy steps again to generate and deploy the latest code

# TODO

[ ] Add Rasa-X functionality for live training