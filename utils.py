from datetime import datetime
from loguru import logger

from db import session, Log, User

# Запись сохраненных в бд юзеров и логов в лог файл
logger.add('info.log', format="{message}", level="DEBUG")


def get_url(date_str):
    """Формирование окончательного урла для получения логов
    по заданной дате"""
    return 'http://www.dsdev.tech/logs/' + str(date_str)


def correct_time(lst):
    """Приведение даты к формату datetime"""
    def apply(x):
        x['created_at'] = datetime.strptime(x['created_at'].replace("T", " "), '%Y-%m-%d %H:%M:%S')
        return x
    return map(apply, lst)


def save_log(message, created_at, user_id):
    """Сохранение лога в БД"""
    logs_exists = session.query(Log).filter(created_at == Log.created_at).count()
    if not logs_exists:
        new_log = Log(message=message, created_at=created_at, user_id=int(user_id))
        session.add(new_log)
        session.commit()
        logger.debug(f'Лог созданный в {created_at} пользователем {user_id} сохранен!')


def save_user(first_name, second_name, user_id):
    """Сохранение юзера в БД"""
    users_exists = session.query(User).filter(User.user_id == user_id).count()
    if not users_exists:
        new_user = User(user_id=int(user_id), first_name=first_name, second_name=second_name)
        session.add(new_user)
        session.commit()
        logger.info(f'Пользователь: {first_name} {second_name} с {user_id} сохранен!')


def sort_by_created_at(nums):
    """Пирамидальная сортировка списка логов по created_at значению"""
    n = len(nums)
    for i in range(n, -1, -1):
        heapify(nums, n, i)

    for i in range(n - 1, 0, -1):
        nums[i], nums[0] = nums[0], nums[i]
        heapify(nums, i, 0)


def heapify(nums, heap_size, root_index):

    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2

    if left_child < heap_size and nums[left_child]['created_at'] > nums[largest]['created_at']:
        largest = left_child

    if right_child < heap_size and nums[right_child]['created_at'] > nums[largest]['created_at']:
        largest = right_child

    if largest != root_index:
        nums[root_index], nums[largest] = nums[largest], nums[root_index]
        heapify(nums, heap_size, largest)