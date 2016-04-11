# -*- coding: utf-8 -*-



import pytz
from datetime import datetime
from pytz import timezone

is_timezone_unknown = (session.user_timezone is None)

def getLocalTimeStr(utc_time):
    is_timezone_unknown = (session.user_timezone is None)
    client_local_timezone = session.user_timezone or 'UTC'
    utc_time = pytz.utc.localize(utc_time)
    local_time = utc_time.astimezone(pytz.timezone(client_local_timezone))
    return local_time.strftime(DATETIME_FORMAT)
