import itertools
import math

def detect_arbitrage(exchange_rates):
    """
    Detects if there is an arbitrage opportunity given exchange rates and identifies the cycle.
    Uses the Bellman-Ford algorithm on a log-transformed graph.
    
    :param exchange_rates: A 2D list representing exchange rates between currencies as a matrix.
    :return: A tuple (True, cycle) if an arbitrage opportunity exists, (False, None) otherwise.
    """
    num_currencies = len(exchange_rates)
    
    # log transform the weights
    log_exchange_rates = [[-math.log(rate) for rate in row] for row in exchange_rates]
    
    for start_currency in range(num_currencies):
        min_dist = [float('inf')] * num_currencies
        predecessor = [-1] * num_currencies
        min_dist[start_currency] = 0
        
        # Relax edges (v-1) times
        for _ in range(num_currencies - 1):
            for source, dest in itertools.product(range(num_currencies), repeat=2):
                if min_dist[dest] > min_dist[source] + log_exchange_rates[source][dest]:
                    min_dist[dest] = min_dist[source] + log_exchange_rates[source][dest]
                    predecessor[dest] = source
        
        # check if there are still relaxble edges, implying a negative cycle 
        for source, dest in itertools.product(range(num_currencies), repeat=2):
            if min_dist[dest] > min_dist[source] + log_exchange_rates[source][dest]:
                # negative cycle exists, use predecessor chain to print it
                cycle = []
                visited = set()
                current = dest
                while current not in visited:
                    visited.add(current)
                    current = predecessor[current]
                cycle_start = current
                cycle.append(cycle_start)
                current = predecessor[current]
                while current != cycle_start:
                    cycle.append(current)
                    current = predecessor[current]
                cycle.append(cycle_start)
                return True, list(reversed(cycle))
    
    return False, None

# Example input for csc3025 arbitrage project
exchange_rates = [
    [1.0000, 1.1989, 1.2437, 1.7850],  # Currency GBP to GBP, EUR, USD, CAD
    [0.8341, 1.0000, 0.9913, 1.4888],  # Currency EUR to GBP, EUR, USD, CAD
    [0.8041, 1.0088, 1.0000, 1.4350],  # Currency USD to GBP, EUR, USD, CAD
    [0.5602, 0.6717, 0.6968, 1.0000]   # Currency CAD to GBP, EUR, USD, CAD
]

# Check for arbitrage
arbitrage, cycle = detect_arbitrage(exchange_rates)
if arbitrage:
    print("Arbitrage opportunity exists! Cycle:", cycle)
else:
    print("No arbitrage opportunity.")
