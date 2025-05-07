import time

class DNSCache:
    def __init__(self):
        self.cache = {}
        self.hits = 0
        self.misses = 0

    def set(self, domain, response, ttl):
        expiry = time.time() + ttl
        self.cache[domain] = (response, expiry)

    def get(self, domain):
        entry = self.cache.get(domain)
        if not entry:
            self.misses += 1
            return None

        response, expiry = entry
        if time.time() < expiry:
            self.hits += 1
            return response
        else:
            del self.cache[domain]
            self.misses += 1
            return None

    def __contains__(self, domain):
        return domain in self.cache and time.time() < self.cache[domain][1]

    def stats(self):
        return {'hits': self.hits, 'misses': self.misses}

    def __contains__(self, domain):
        """Check if a domain is in the cache and not expired."""
        return domain in self.cache and time.time() < self.cache[domain][1]
