import threading
import dns.message
import dns.query
from utils import extract_ttl  # Make sure utils.py is present and this function works
import time

class Prefetcher:
    def __init__(self, predictor, cache=None, upstream_dns='1.1.1.1'):
        self.predictor = predictor
        self.cache = cache  # Should be an instance of DNSCache
        self.upstream_dns = upstream_dns

    def prefetch_from(self, current_domain, top_k=2):
        """Predict the next likely domains and prefetch them in the background."""
        predicted_domains = self.predictor.predict(current_domain, top_k=top_k)
        for domain in predicted_domains:
            thread = threading.Thread(target=self._prefetch_domain, args=(domain,))
            thread.daemon = True  # Background thread won't block the main thread
            thread.start()

    def _prefetch_domain(self, domain):
        try:
            print(f"[~] Prefetching {domain}")
            query = dns.message.make_query(domain, dns.rdatatype.A)
            response = dns.query.udp(query, self.upstream_dns, timeout=2)

            if self.cache is not None:
                ttl = extract_ttl(response)
                self.cache.set(domain, response, ttl=ttl)
                print(f"[+] Prefetched and cached {domain} with TTL={ttl}")
            else:
                print(f"[+] Prefetched {domain} (not cached)")

        except Exception as e:
            print(f"[!] Failed to prefetch {domain}: {e}")
