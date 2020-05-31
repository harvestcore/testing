import docker

from config.server_environment import DOCKER_BASE_URL, DOCKER_ENABLED


class DockerEngine:
    client = docker.DockerClient(base_url=DOCKER_BASE_URL)
    engine = None

    def __new__(cls, *args, **kwargs):
        if not cls.engine:
            cls.engine = super(DockerEngine, cls).__new__(cls, *args, **kwargs)
        return cls.engine

    """
        Get the current Docker client.
    """
    def get_client(self):
        return self.client if self.engine else None

    """
        Runs an operation in the containers context.
    """
    def run_container_operation(self, operation, data):
        try:
            return getattr(self.get_client().containers, operation)(**data)
        except docker.errors.APIError:
            return False

    """
        Runs an operation in the images context.
    """
    def run_image_operation(self, operation, data):
        try:
            return getattr(self.get_client().images, operation)(**data)
        except docker.errors.APIError:
            return False

    """
        Returns the container that has the given id.
    """
    def get_container_by_id(self, container_id):
        try:
            return self.get_client().containers.get(container_id=container_id)
        except docker.errors.APIError:
            return False

    """
        Runs an operation in the given object. The object can be an image or
        a container.
    """
    @staticmethod
    def run_operation_in_object(object, operation, data):
        try:
            return getattr(object, operation)(**data)
        except docker.errors.APIError:
            return False

    """
        Returns the image that has the given name.
    """
    def get_image_by_name(self, name):
        try:
            return self.get_client().images.get(name=name)
        except docker.errors.APIError:
            return False

    """
        Returns the current status of the Docker client.
    """
    def status(self):
        if DOCKER_ENABLED:
            try:
                return {
                    'is_up': self.get_client().ping(),
                    'data_usage': self.get_client().df(),
                    'info': self.get_client().info()
                }
            except docker.errors.APIError:
                return {
                    'status': False,
                    'disabled': False,
                    'msg': 'Docker is not working properly'
                }
        else:
            return {
                'status': False,
                'disabled': True,
                'msg': 'Docker is not enabled'
            }
