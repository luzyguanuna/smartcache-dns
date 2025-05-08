# SmartCache DNS

This repository contains the implementation for our CS1430 final project: **SmartCache DNS**, a predictive, personalized DNS resolution system.

## Overview

SmartCache DNS is a DNS proxy that:
- Intercepts DNS queries
- Caches responses with TTL awareness
- Predicts the next likely domain using a personalized Markov model
- Prefetches likely future domains in the background to improve cache hit rates and reduce DNS resolution latency

## Features

- Markov chain-based prediction of domain transitions
- Prefetching based on predicted next domains
- User-personalized modeling and online learning
- TTL-aware caching with expiration enforcement
- Multithreaded design with background prefetching

## File Structure

| File | Description |
|------|-------------|
| `dns_proxy.py` | Main proxy logic: handles incoming queries, caching, prediction, and upstream resolution |
| `cache.py` | Implements a DNS response cache with TTL-based expiration and hit/miss tracking |
| `domain_predictor.py` | Learns domain-to-domain transitions using a first-order Markov model |
| `prefetcher.py` | Spawns background threads to prefetch predicted domains |
| `utils.py` | Utility functions including TTL extraction and optional LRU caching logic |

## Requirements

- Python 3.7+
- `dnspython` library  
  Install with:
  ```bash
  pip install dnspython


## Running the System

1. **Start the DNS proxy:**

   Open a terminal and run:

   ```bash
   python3 dns_proxy.py

You should see something like...

[+] SmartCache DNS proxy running on 127.0.0.1:53536

2. **In a second terminal, run DNS queries through the proxy using dig:**

dig @127.0.0.1 -p 53536 canvas.harvard.edu

3. **Try a sequence of domains (e.g., Harvard-related services):**
dig @127.0.0.1 -p 53536 zoom.us
dig @127.0.0.1 -p 53536 gmail.com
dig @127.0.0.1 -p 53536 piazza.com

4. **Watch the terminal for real-time output:**
You'll see cache hits, misses, TTLs, and prefetch activity like:

[?] Checking cache for gmail.com
[✓] Cache HIT for gmail.com
[~] Prefetching piazza.com
[CACHE] Stats → Hits: 3, Misses: 2
