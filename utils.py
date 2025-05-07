from collections import OrderedDict
import time
import dns.rdatatype

class TTLCache:
    def __init__(self, capacity):
        # Max number of entries in the cache
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """Retrieve a value from the cache if it hasn’t expired."""
        if key in self.cache:
            value, expire_time = self.cache[key]
            if time.time() < expire_time:
                # Mark as recently used
                self.cache.move_to_end(key)
                return value
            else:
                # Remove expired item
                del self.cache[key]
        return None

    def put(self, key, value, ttl):
        """Add a new value to the cache or update an existing one."""
        expire_time = time.time() + ttl
        if key in self.cache:
            del self.cache[key]  # Overwrite existing key
        elif len(self.cache) >= self.capacity:
            # Remove the least recently used item
            self.cache.popitem(last=False)
        self.cache[key] = (value, expire_time)

    def __len__(self):
        """Return number of valid (non-expired) entries."""
        return len(self.cache)

def extract_ttl(response):
    """
    Extracts the minimum TTL from a DNS response.
    Safely handles all record types, including CNAME.
    """
    try:
        ttls = [rrset.ttl for rrset in response.answer if hasattr(rrset, 'ttl')]
        return min(ttls) if ttls else 60
    except Exception as e:
        print(f"[WARN] Failed to extract TTL: {e}")
        return 60
