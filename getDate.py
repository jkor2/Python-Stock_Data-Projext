from datetime import datetime, timedelta


def get_current_date():
    """
    Gets current date and returns proper format
    """
    current_date = datetime.now()
    return current_date


def seven_days_ago():
    """
    Gets date from 7 days ago and return the proper format
    """

    current_date = datetime.now()
    seven_days = current_date - timedelta(days=7)
    return seven_days
