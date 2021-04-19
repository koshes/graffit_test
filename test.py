from unittest import TestCase
from unittest.mock import patch, Mock


class TestLog(TestCase):

    @patch('main.GetLog')
    def test_log_get_json(self, MockLog):
        """тест: проверка принимаемых данных полученных по апи"""
        log = MockLog(20210123)

        log.get_json.return_value = [
            {
                'created_at': '2021-01-23T20:52:21',
                'first_name': 'Эльдар',
                'message': "Mr. Frodo? That blade was broken! Where is he? Where is Gondor's finest? Where's my first-born?",
                'second_name': 'Хохлов',
                'user_id': '367083'
            }
        ]

        response = log.get_json()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)

