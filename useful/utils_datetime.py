from dateutil.parser import parse, ParserError
from datetime import datetime as DT, timedelta as TD
from logging import error


def normalize_datetime(date=DT.now(), days_ago=0, date_format='%Y-%m-%d %H:%M:%S', format=True):
    try:
        parse_date = parse(date)
    except ParserError:
        parse_date = DT.strptime(date, '%H%M%S')
    except TypeError:
        parse_date = date
    except Exception as err:
        error(err)
    dt = parse_date - TD(days=int(days_ago))
    dt = dt.strftime(date_format)
    if format is False:
        dt = parse(dt)
    return dt

def date_range(date, **kwargs):
    date = normalize_datetime(date)
    try:
        days_ago = kwargs.get('days_ago')
        start_date = normalize_datetime(days_ago=days_ago)
        end_date = normalize_datetime()
    except TypeError:
        start_date = normalize_datetime(date=kwargs.get('start_date'))
        end_date = normalize_datetime(date=kwargs.get('end_date'))
    if date >= start_date and date <= end_date:
        return True
    else:
        return False

