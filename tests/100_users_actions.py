from locust import HttpUser, task, between
import test_data
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
                    response.success()
                else:
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
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
                    response.success()
                else:
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
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
                    response.success()
                else:
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
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
                    response.success()
                else:
                    response.failure(f'response status codes are {response_code_1, response_code_2}')
            else:
                response.failure(f'server status code is {response.status_code}')


class User_1(User_admin):
    login_index = 1


class User_2(User_admin):
    login_index = 2


class User_3(User_admin):
    login_index = 3


class User_4(User_admin):
    login_index = 4


class User_5(User_admin):
    login_index = 5


class User_6(User_admin):
    login_index = 6


class User_7(User_admin):
    login_index = 7


class User_8(User_admin):
    login_index = 8


class User_9(User_admin):
    login_index = 9


class User_10(User_admin):
    login_index = 10


class User_11(User_admin):
    login_index = 11


class User_12(User_admin):
    login_index = 12


class User_13(User_admin):
    login_index = 13


class User_14(User_admin):
    login_index = 14


class User_15(User_admin):
    login_index = 15


class User_16(User_admin):
    login_index = 16


class User_17(User_admin):
    login_index = 17


class User_18(User_admin):
    login_index = 18


class User_19(User_admin):
    login_index = 19


class User_20(User_admin):
    login_index = 20


class User_21(User_admin):
    login_index = 21


class User_22(User_admin):
    login_index = 22


class User_23(User_admin):
    login_index = 23


class User_24(User_admin):
    login_index = 24


class User_25(User_admin):
    login_index = 25


class User_26(User_admin):
    login_index = 26


class User_27(User_admin):
    login_index = 27


class User_28(User_admin):
    login_index = 28


class User_29(User_admin):
    login_index = 29


class User_30(User_admin):
    login_index = 30


class User_31(User_admin):
    login_index = 31


class User_32(User_admin):
    login_index = 32


class User_33(User_admin):
    login_index = 33


class User_34(User_admin):
    login_index = 34


class User_35(User_admin):
    login_index = 35


class User_36(User_admin):
    login_index = 36


class User_37(User_admin):
    login_index = 37


class User_38(User_admin):
    login_index = 38


class User_39(User_admin):
    login_index = 39


class User_40(User_admin):
    login_index = 40


class User_41(User_admin):
    login_index = 41


class User_42(User_admin):
    login_index = 42


class User_43(User_admin):
    login_index = 43


class User_44(User_admin):
    login_index = 44


class User_45(User_admin):
    login_index = 45


class User_46(User_admin):
    login_index = 46


class User_47(User_admin):
    login_index = 47


class User_48(User_admin):
    login_index = 48


class User_49(User_admin):
    login_index = 49


class User_50(User_admin):
    login_index = 50


class User_51(User_admin):
    login_index = 51


class User_52(User_admin):
    login_index = 52


class User_53(User_admin):
    login_index = 53


class User_54(User_admin):
    login_index = 54


class User_55(User_admin):
    login_index = 55


class User_56(User_admin):
    login_index = 56


class User_57(User_admin):
    login_index = 57


class User_58(User_admin):
    login_index = 58


class User_59(User_admin):
    login_index = 59


class User_60(User_admin):
    login_index = 60


class User_61(User_admin):
    login_index = 61


class User_62(User_admin):
    login_index = 62


class User_63(User_admin):
    login_index = 63


class User_64(User_admin):
    login_index = 64


class User_65(User_admin):
    login_index = 65


class User_66(User_admin):
    login_index = 66


class User_67(User_admin):
    login_index = 67


class User_68(User_admin):
    login_index = 68


class User_69(User_admin):
    login_index = 69


class User_70(User_admin):
    login_index = 70


class User_71(User_admin):
    login_index = 71


class User_72(User_admin):
    login_index = 72


class User_73(User_admin):
    login_index = 73


class User_74(User_admin):
    login_index = 74


class User_75(User_admin):
    login_index = 75


class User_76(User_admin):
    login_index = 76


class User_77(User_admin):
    login_index = 77


class User_78(User_admin):
    login_index = 78


class User_79(User_admin):
    login_index = 79


class User_80(User_admin):
    login_index = 80


class User_81(User_admin):
    login_index = 81


class User_82(User_admin):
    login_index = 82


class User_83(User_admin):
    login_index = 83


class User_84(User_admin):
    login_index = 84


class User_85(User_admin):
    login_index = 85


class User_86(User_admin):
    login_index = 86


class User_87(User_admin):
    login_index = 87


class User_88(User_admin):
    login_index = 88


class User_89(User_admin):
    login_index = 89


class User_90(User_admin):
    login_index = 90


class User_91(User_admin):
    login_index = 91


class User_92(User_admin):
    login_index = 92


class User_93(User_admin):
    login_index = 93


class User_94(User_admin):
    login_index = 94


class User_95(User_admin):
    login_index = 95


class User_96(User_admin):
    login_index = 96


class User_97(User_admin):
    login_index = 97


class User_98(User_admin):
    login_index = 98


class User_99(User_admin):
    login_index = 99
