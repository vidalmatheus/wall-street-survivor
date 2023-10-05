import pytz
from django.utils import timezone


def to_tz(d, tz):
    if d is None:
        return None
    ptz = pytz.timezone(tz)
    if timezone.is_aware(d):
        return d.astimezone(ptz)
    return ptz.localize(d)
