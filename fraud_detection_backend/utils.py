from time import strftime, localtime

def format_date(datetime_in_epoch):
    return strftime('%Y-%m-%d', localtime(datetime_in_epoch))
