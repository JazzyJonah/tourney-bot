def convert(dateTime, timezone):
    dateTimePattern = "%m/%d/%Y %H:%M:%S"
    if timezone == "EST":
        timezone = -4
    if timezone == "GMT":
        timezone = 0
    return str(int(time.mktime(time.strptime(dateTime, dateTimePattern)))-3600*timezone)