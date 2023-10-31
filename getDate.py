from datetime import datetime, timedelta


def get_current_date():
    """
    Gets current date and returns proper format
    """
    current_date = datetime.now()
    seven_days = current_date - timedelta(days=7)
    seven_days, current_date


print(get_current_date())
