from core.wss import wss_endpoints
from memoize import memoize

BASE_URL = "https://app.wallstreetsurvivor.com"

class WssAPI():

    def __repr__(self):
        return f"Repr_{self.__class__.__name__}"
    
    @property
    def base_url(self):
        return BASE_URL

    @property
    def get_auth_token(self):
        return None # Memcache

    @memoize(timeout=10)
    def get_transactions(self, start_date, end_date):
        resp = wss_endpoints.GetTransactions(self).send(start_date, end_date)
        return resp.parsed
    

