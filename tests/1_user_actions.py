from locust import HttpUser, task, between
import test_data

orders_list = []


class User_admin(HttpUser):
    host = "https://api.laxo.one/"
    wait_time = between(1, 2)
    sid_value = 'null'
    # fixed_count = 1
    headers = {'Content-Type': 'application/json', 'Origin': 'https://loadtest.laxo.one',
               'Referer': 'https://loadtest.laxo.one/'}
    login_index = 0
    login_value = test_data.TestData.users_logins[login_index]

    def on_start(self):
        self.login()

    def login(self, null=None):
        body = [{"class": "user_session", "method": "auth", "param": {"login": self.login_value, "pass": "123"},
                 "sid": null}]

        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='login') as response:
            if response.status_code == 200:
                self.sid_value = response.json()[1].get('response').get('sid')
                if self.sid_value != 'null':
                    response.success()
                else:
                    response.failure(f'sid is null')
            else:
                response.failure(f'server status code is {response.status_code}')

    @task(1)
    def add_order(self):
        body = [{
            "class": "order",
            "method": "add",
            "param": {
                "order_name": "new_order",
                "order_sum": 0,
                "order_status_id": "3",
                "funnel_id": "1",
                "contact_id": "1",
                "order_user_mentor": self.login_index
            },
            "sid": self.sid_value
        }]
        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='add_order') as response:
            if response.status_code == 200:
                response_code_1 = response.json()[0].get('code')
                response_code_2 = response.json()[1].get('code')
                if response_code_1 == 200 and response_code_2 == 200:
                    response.success()
                else:
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
                response.failure(f'server status code is {response.status_code}')
