import random
from locust import HttpUser, task, between

API_VER = 'v1'


class AdminApiUser(HttpUser):
    """
    Admin api have 4 interfaces: read_server_status, read_models, create_model, delete_model
    create_model, delete_model are not frequently used in common use cases
    read_server_status is more used
    read_models is the most used
    """
    wait_time = between(2, 5)

    @task(1)
    def get_server_status(self):
        self.client.get(f'/{API_VER}/status')

    @task(20)
    def read_models(self):
        self.client.get(f'/{API_VER}/models')


class MlApiUser(HttpUser):
    wait_time = between(0.1, 1)

    @task(1)
    def invocation(self):
        model = random.choice(
            ['miniloan-linear-svc', 'miniloan-xgb', 'miniloan-rfc', 'miniloan-rfr']
        )

        input_param = [
            {
                "name": "creditScore",
                "value": random.randint(100, 800)
            }, {
                "name": "income",
                "value": random.uniform(18_000.0, 80_000.0)
            }, {
                "name": "loanAmount",
                "value": random.uniform(18_000.0, 160_000.0)
            }, {
                "name": "monthDuration",
                "value": random.randint(1, 120)
            }, {
                "name": "rate",
                "value": random.uniform(0.1, 10.0)
            }
        ]

        self.client.post(
            url=f'/{API_VER}/invocations',
            json={
                "model_name": model,
                "model_version": "v0",
                "params": input_param
            }
        )
