def is_valid_imei(imei: str) -> bool:
    """
    Проверка IMEI.

    Args:
        imei (str): IMEI.

    Returns:
        bool: True - IMEI подходит, False - IMEI не подходит
    """

    return len(imei) == 15 and imei.isdigit()
