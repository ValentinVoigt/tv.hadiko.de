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
