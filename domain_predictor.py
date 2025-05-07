import collections

class DomainPredictor:
    def __init__(self):
        # Tracks how often one domain is followed by another
        self.transition_table = collections.defaultdict(collections.Counter)

    def update(self, prev_domain, next_domain):
        """Update the transition count from prev_domain to next_domain."""
        if prev_domain:
            self.transition_table[prev_domain][next_domain] += 1

    def predict(self, current_domain, top_k=1):
        """Return the top_k most likely next domains based on current_domain."""
        if current_domain not in self.transition_table:
            return []
        next_domains = self.transition_table[current_domain].most_common(top_k)
        return [domain for domain, _ in next_domains]

    def train_on_sequence(self, domain_sequence):
        """Train the predictor on a full sequence of domain accesses."""
        for i in range(len(domain_sequence) - 1):
            self.update(domain_sequence[i], domain_sequence[i + 1])

print("DomainPredictor loaded.")