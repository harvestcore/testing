import os

from src.utils.docker_check import running_in_docker

# Environment variables

# Mongo hostname
MONGO_HOSTNAME = os.environ.get('MONGO_HOSTNAME', 'localhost')

# Mongo port
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)

# IPManager base collection
TESTING_DATABASE = os.environ.get('TESTING_DATABASE', 'ipm_root_testing')
BASE_DATABASE = os.environ.get('BASE_DATABASE', TESTING_DATABASE)

# Password encryption key (testing)
ENC_KEY = os.environ.get(
    'ENC_KEY', 'KM1tL17icOwO7QkzOy4wrTVUSUfr10CEFIFDvAZpI40=').encode()

# JWT encryption key (testing)
JWT_ENC_KEY = os.environ.get(
    'JWT_ENC_KEY', 'G-yEgpe9MNBzRC14UQ_3lHtNkiY6z2enG1KzY33Vcvw=')

DOCKER_BASE_URL = os.environ.get(
    'DOCKER_BASE_URL', 'unix://var/run/docker.sock')

DOCKER_ENABLED = False if \
    running_in_docker() and DOCKER_BASE_URL == 'unix://var/run/docker.sock' \
    else True

ANSIBLE_PATH = os.environ.get('ANSIBLE_PATH', './')
