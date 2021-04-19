import requests
from loguru import logger

from utils import correct_time, get_url, save_log, save_user, sort_by_created_at


class GetLog:
    @logger.catch
    def get_json(self, date):
        """Получение json по заданной дате"""
        try:
            url = get_url(date)
            result = requests.get(url)
            result.encoding = 'utf-8'
            result.raise_for_status()
            return result.json()
        except (requests.RequestException, ValueError):
            print('Ошибка Сети')
            return False

    @logger.catch
    def get_log(self, date):
        """Парсинг json и сохранение данных логов и пользователей в БД"""
        data = self.get_json()
        if 'error' in data:
            logger.debug(data['error'])
        if 'logs' in data:
            # Получение всех логов с форматированным временем
            all_logs = list(correct_time(data['logs']))
            sort_by_created_at(all_logs)
            for log in all_logs:
                first_name = log['first_name']
                second_name = log['second_name']
                user_id = log['user_id']
                message = log['message']
                created_at = log['created_at']
                save_user(first_name, second_name, user_id)
                save_log(message, created_at, user_id)
            logger.info(f'Запись завершена')

