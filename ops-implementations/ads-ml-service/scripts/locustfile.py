import random

import locust

API_VER = 'v1'


class ApiUser(locust.HttpUser):
    wait_time = locust.between(0.1, 0.5)

    @locust.task(5)
    def read_models(self):
        self.client.get('/models')

    @locust.task(100)
    def invocation(self):
        self.client.post(
            url='/predictions',
            json={
                'parameters': [
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
                ],
                'target': [
                    {
                        'rel': 'endpoint',
                        'href': f'/endpoints/{random.randint(1, 4)}'
                    }
                ]
            }
        )
