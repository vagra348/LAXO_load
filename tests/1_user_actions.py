from locust import HttpUser, task, between
import config
import random as rnd

orders_id_list = []
contacts_id_list = [1]

class User_admin(HttpUser):
    host = "https://api.laxo.one/"
    wait_time = between(1, 2)
    sid_value = 'null'
    fixed_count = 1
    headers = {'Content-Type': 'application/json', 'Origin': 'https://loadtest.laxo.one',
               'Referer': 'https://loadtest.laxo.one/'}
    login_index = 0
    login_value = config.TestData.users_logins[login_index]

    def on_start(self):
        self.login()

    def login(self, null=None):
        body = [{"class": "user_session", "method": "auth", "param": {"login": self.login_value, "pass": "123"},
                 "sid": null}]

        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='login') as response:
            if response.status_code == 200:
                self.sid_value = response.json()[1].get('response').get('sid')
                if self.sid_value != 'null':
                    config.logger.debug(f"Success login" + " User " + str(self.login_index))
                    response.success()
                else:
                    response.failure(f'sid is null')
            elif response.status_code == 401:
                config.logger.debug(f"LOGIN RECURSION" + " User " + str(self.login_index))
                self.login()
            else:
                config.logger.debug(f"FAILED SERVER" + " User " + str(self.login_index))
                response.failure(f'server status code is {response.status_code}')

    @task(2)
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
                "order_user_mentor": str(self.login_index)
            },
            "sid": str(self.sid_value)
        }]
        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='add_order') as response:
            if response.status_code == 200:
                response_code_1 = response.json()[0].get('code')
                response_code_2 = response.json()[1].get('code')
                if response_code_1 == 200 and response_code_2 == 200:
                    orders_id_list.append(response.json()[0].get('response'))
                    config.logger.debug(f"Success order add" + " User " + str(self.login_index))
                    response.success()
                else:
                    config.logger.debug(f"FAILED ORDER ADD" + " User " + str(self.login_index))
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
                config.logger.debug(f"FAILED SERVER" + " User " + str(self.login_index))
                response.failure(f'server status code is {response.status_code}')

    @task(7)
    def read_order(self):
        if len(orders_id_list) == 0:
            return
        order_id = rnd.choice(orders_id_list)
        body = [
            {
                "class": "order",
                "method": "get",
                "param": str(order_id),
                "sid": str(self.sid_value)
            }
        ]
        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='read_order') as response:
            if response.status_code == 200:
                response_code_1 = response.json()[0].get('code')
                response_code_2 = response.json()[1].get('code')
                if response_code_1 == 200 and response_code_2 == 200:
                    config.logger.debug(f"Success order read" + " User " + str(self.login_index))
                    response.success()
                else:
                    config.logger.debug(f"FAILED ORDER READ" + " User " + str(self.login_index))
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
                config.logger.debug(f"FAILED SERVER" + " User " + str(self.login_index))
                response.failure(f'server status code is {response.status_code}')

    @task(1)
    def add_contact(self, false=False, true=True, null=None):
        body = [
            {
                "class": "contact",
                "method": "add",
                "param": {
                    "contact_name": "ННННН",
                    "field": [
                        {
                            "field_id": "2",
                            "field_name": "organisation",
                            "field_view_name": "Цветы 24",
                            "field_type_id": "9",
                            "field_sub_type_id": "2",
                            "field_min_count": "0",
                            "field_max_count": "1",
                            "field_icon_name": null,
                            "field_priority": "0",
                            "mockSelect": [
                                {
                                    "field_value_id": "71",
                                    "value": "Новая",
                                    "new": 1
                                },
                                {
                                    "value": "Нагрузочность",
                                    "field_value_id": "7",
                                    "field_id": "2"
                                }
                            ],
                            "changed": false,
                            "touched": true,
                            "edited": false,
                            "value": [
                                {
                                    "field_value_id": "71",
                                    "value": "Новая",
                                    "new": 1
                                }
                            ]
                        },
                        {
                            "field_id": "1",
                            "field_name": "post",
                            "field_view_name": "Должность",
                            "field_type_id": "2",
                            "field_sub_type_id": null,
                            "field_min_count": "0",
                            "field_max_count": "0",
                            "field_icon_name": null,
                            "field_priority": "0",
                            "changed": false,
                            "touched": true,
                            "edited": false,
                            "value": "контрагентик"
                        },
                        {
                            "field_id": "3",
                            "field_name": "phone_number",
                            "field_view_name": "Телефон",
                            "field_type_id": "13",
                            "field_sub_type_id": "1",
                            "field_min_count": "0",
                            "field_max_count": "5",
                            "field_icon_name": "phone_number",
                            "field_priority": "0",
                            "section": 2,
                            "changed": false,
                            "touched": true,
                            "edited": false,
                            "value": "79991234567",
                            "full": false
                        },
                        {
                            "field_id": "5",
                            "field_name": "email",
                            "field_view_name": "Почта",
                            "field_type_id": "12",
                            "field_sub_type_id": "1",
                            "field_min_count": "0",
                            "field_max_count": "5",
                            "field_icon_name": "email",
                            "field_priority": "0",
                            "section": 2,
                            "changed": false,
                            "touched": true,
                            "edited": false,
                            "value": "asdf@asdf.asdf",
                            "full": false
                        }
                    ]
                },
                "sid": str(self.sid_value)
            }
        ]
        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='add_contact') as response:
            if response.status_code == 200:
                response_code_1 = response.json()[0].get('code')
                response_code_2 = response.json()[1].get('code')
                if response_code_1 == 200 and response_code_2 == 200:
                    contacts_id_list.append(response.json()[0].get('response'))
                    config.logger.debug(f"Success contact add" + " User " + str(self.login_index))
                    response.success()
                else:
                    config.logger.debug(f"FAILED CONTACT ADD" + " User " + str(self.login_index))
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
                config.logger.debug(f"FAILED SERVER" + " User " + str(self.login_index))
                response.failure(f'server status code is {response.status_code}')

    @task(4)
    def read_contact(self):
        if len(contacts_id_list) == 0:
            return
        contact_id = rnd.choice(contacts_id_list)
        body = [
            {
                "class": "contact",
                "method": "get",
                "param": str(contact_id),
                "sid": str(self.sid_value)
            }
        ]
        with self.client.post(f"/", headers=self.headers, json=body, catch_response=True, name='read_contact') as response:
            if response.status_code == 200:
                response_code_1 = response.json()[0].get('code')
                response_code_2 = response.json()[1].get('code')
                if response_code_1 == 200 and response_code_2 == 200:
                    config.logger.debug(f"Success contact read" + " User " + str(self.login_index))
                    response.success()
                else:
                    config.logger.debug(f"FAILED CONTACT READ" + " User " + str(self.login_index))
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
                config.logger.debug(f"FAILED SERVER" + " User " + str(self.login_index))
                response.failure(f'server status code is {response.status_code}')

