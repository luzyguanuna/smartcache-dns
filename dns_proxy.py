import socket
import dns.message
import dns.query
from domain_predictor import DomainPredictor
from prefetcher import Prefetcher
from cache import DNSCache
from utils import extract_ttl  # Safely extract TTLs from responses

# Config
LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 53536
UPSTREAM_DNS = '1.1.1.1'

# DNS system components
predictor = DomainPredictor()
cache = DNSCache()
prefetcher = Prefetcher(predictor, cache=cache)

last_domain = None  # For building query sequences

# Set up UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"[+] SmartCache DNS proxy running on {LISTEN_IP}:{LISTEN_PORT}")

while True:
    try:
        # Receive DNS query
        data, client_addr = sock.recvfrom(512)
        query = dns.message.from_wire(data)
        current_domain = str(query.question[0].name).rstrip('.')  # Normalize domain

        print(f"[>] Query from {client_addr}: {current_domain}")
        print(f"[?] Checking cache for {current_domain}")

        # Check the cache first
        cached_response = cache.get(current_domain)
        if cached_response:
            print(f"[✓] Cache HIT for {current_domain}")
            sock.sendto(cached_response.to_wire(), client_addr)
        else:
            print(f"[✗] Cache MISS → sending to upstream for {current_domain}")
            response = dns.query.udp(query, UPSTREAM_DNS, timeout=2)
            sock.sendto(response.to_wire(), client_addr)
            print(f"[<] Response received from upstream for {current_domain}")

            # Extract TTL safely and cache
            min_ttl = extract_ttl(response)
            print(f"[+] Caching response for {current_domain} with TTL={min_ttl}")
            cache.set(current_domain, response, ttl=min_ttl)

        # Update predictor and prefetch in background
        if last_domain:
            predictor.update(last_domain, current_domain)
        last_domain = current_domain

        prefetcher.prefetch_from(current_domain)

        # Log cache stats
        stats = cache.stats()
        print(f"[CACHE] Stats → Hits: {stats['hits']}, Misses: {stats['misses']}")

    except Exception as e:
        print(f"[!] Error handling request: {e}")
