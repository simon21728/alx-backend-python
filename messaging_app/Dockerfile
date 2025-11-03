FROM jenkins/jenkins:lts

USER root

# Install Python 3 and venv
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

