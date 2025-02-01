import time
import json
import requests
from typing import Union

from config import CONFIG


class CheckIMEI:
    """Класс проверки IMEI"""

    URL_FOR_SERVICE = 'https://api.imeicheck.net/v1/services'
    URL_FOR_ORDERS = 'https://api.imeicheck.net/v1/orders'
    HEADERS = {
        'Authorization': f'Bearer {CONFIG["API_TOKEN_SERVICE"]}',
        'Content-Type': 'application/json'
    }

    def __init__(self, imei: str, request_api: bool = None) -> None:
        """Инициализация параметров"""

        self.imei = imei
        self.request_api = request_api

    def _get_available_services(self) -> Union[json, None]:
        """
        Получение сервисов

        Returns:
            json: JSON с доступными сервисами
            None: В случае ошибки
        """

        try:
            response = requests.get(self.URL_FOR_SERVICE, headers=self.HEADERS)
            response.raise_for_status()
            return response.json()

        # TODO: Можно описать все ошибки и добавить логгер
        except Exception as ex:
            print(f"Произошла ошибка: {ex}")

            return None

    def _create_order(self) -> Union[json, None]:
        """
        Создание запроса

        Returns:
            json: JSON с информацией о заказе
            None: В случае ошибки
        """

        services = self._get_available_services()
        if services:
            service_id = services[0]['id']  # Выбираем первый сервис из списка для теста
            url = self.URL_FOR_ORDERS
            headers = {
                'Authorization': f'Bearer {CONFIG["API_TOKEN_SERVICE"]}',
                'Accept-Language': 'en',
                'Content-Type': 'application/json'
            }
            data = {
                "deviceIds": [self.imei],
                "serviceId": service_id,
                "duplicateProcessingType": "reprocess"
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                return response.json()

            # TODO: Можно описать все ошибки и добавить логгер
            except Exception as ex:
                print(f"Произошла ошибка: {ex}")

                return None

    def _get_check_result(self, check_id: str) -> Union[json, None]:
        """
        Получение результатов проверки

        Args:
            check_id (str): ID запроса.

        Returns:
            json: JSON с результатами проверки
            None: В случае ошибки
        """
        try:
            response = requests.get(f"https://api.imeicheck.net/v1/checks/{check_id}", headers=self.HEADERS)
            response.raise_for_status()
            return response.json()

        # TODO: Можно описать все ошибки и добавить логгер
        except Exception as ex:
            print(f"Произошла ошибка: {ex}")

            return None

    def _result_data(self, data: json) -> str:
        """
        Формирование ответа для пользователя

        Args:
            data (json): Данные, полученные от запроса.

        Returns:
            str: Ответ для пользователя
        """
        return (
            f"Результаты проверки IMEI {self.imei}:\n\n"
            f"Устройство: {data['properties'].get('deviceName', 'Неизвестно')}\n\n"
            f"Изображение: {data['properties'].get('image', 'Неизвестно')}\n\n"
            f"IMEI: {data['properties'].get('imei', 'Неизвестно')}\n\n"
            f"MEID: {data['properties'].get('meid', 'Неизвестно')}\n\n"
            f"IMEI2: {data['properties'].get('imei2', 'Неизвестно')}\n\n"
            f"Серийный номер: {data['properties'].get('serial', 'Неизвестно')}\n\n"
            f"Предполагаемая дата покупки: {data['properties'].get('estPurchaseDate', 'Неизвестно')}\n\n"
            f"GSMA Blacklisted: {data['properties'].get('gsmaBlacklisted', 'Неизвестно')}\n\n"
            f"SIM Lock: {data['properties'].get('simLock', 'Неизвестно')}\n\n"
            f"Статус гарантии: {data['properties'].get('warrantyStatus', 'Неизвестно')}\n\n"
            f"Покрытие ремонта: {data['properties'].get('repairCoverage', 'Неизвестно')}\n\n"
            f"Техническая поддержка: {data['properties'].get('technicalSupport', 'Неизвестно')}\n\n"
            f"Регион Apple: {data['properties'].get('apple/region', 'Неизвестно')}\n\n"
            f"Статус блокировки в США: {data['properties'].get('usaBlockStatus', 'Неизвестно')}\n\n"
            f"Сеть: {data['properties'].get('network', 'Неизвестно')}\n\n"
        )

    def get_data_imei(self) -> str:
        """
        Получение данных IMEI

        Returns:
            str: Ответ для пользователя
        """

        order_info = self._create_order()
        if order_info:
            check_id = order_info['checks'][0]['id']

            time.sleep(10)  # Ожидание обработки запроса

            check_result = self._get_check_result(check_id)
            if check_result:
                if self.request_api:
                    return check_result
                else:
                    return self._result_data(data=check_result)
            else:
                return 'Не удалось получить результаты проверки'
        else:
            return 'Сервис недоступен, попробуйте позже'
