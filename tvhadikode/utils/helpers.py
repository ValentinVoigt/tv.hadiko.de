# -*- encoding: utf-8 -*-

from datetime import datetime

def smartdate(dt):
    """
    Returns the best possible date format.
    @todo localization
    """
    now = datetime.now()
    if dt.date() < now.date():
        if (now.date() - dt.date()).days == 1:
            if (now - dt).seconds < 60*60*8: # near-past events
                return dt.strftime('%H:%M')
            else:
                return dt.strftime('gestern, %H:%M')
        elif (now.date() - dt.date()).days == 1:
            return dt.strftime('vorgestern, %H:%M')
        else:
            return dt.strftime('%d.%m.%Y, %H:%M')
    elif dt.date() == now.date():
        return dt.strftime('%H:%M')
    else:
        if (dt.date() - now.date()).days == 1:
            if (dt - now).seconds < 60*60*8: # near-future events
                return dt.strftime('%H:%M')
            else:
                return dt.strftime('morgen, %H:%M')
        elif (dt.date() - now.date()).days == 2:
            return dt.strftime('übermorgen, %H:%M')
        else:
            return dt.strftime('%d.%m.%Y, %H:%M')

def short_duration(duration):
    """
    Returns a human-readable representation of the given duration (in seconds).
    Duration does not have to be exact.
    """
    if duration < 60:
        return "%is" % duration
    elif duration < 60*60:
        return "%im" % (duration // 60)
    elif duration < 60*60*24:
        return "%ih %im" % divmod(duration // 60, 60)
    return "%id %ih" % divmod(duration // (60*60), 24)
