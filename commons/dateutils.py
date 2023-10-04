import pytz
from django.utils import timezone


def to_tz(d, tz):
    if d is None:
        return None
    ptz = pytz.timezone(tz)
    return d.astimezone(ptz) if timezone.is_aware(d) else ptz.localize(d)
