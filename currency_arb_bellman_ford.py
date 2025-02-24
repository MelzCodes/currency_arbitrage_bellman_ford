import math
import pandas as pd

def convert_to_log_matrix(exchange_rates, currency_names):
    log_exchange_rates = [[-math.log(rate) for rate in row] for row in exchange_rates]
    return pd.DataFrame(log_exchange_rates, index=currency_names, columns=currency_names)

def Bellman_Ford_Arbitrage(rates_matrix, log_margin=0.001):    
    currencies = rates_matrix.index
    num_currencies = len(rates_matrix)
    
    source = 0  # Start from GBP
    min_dist = [float('inf')] * num_currencies

    # List of 'father-nodes'
    predecessor = [-1] * num_currencies
    min_dist[source] = 0

    # Relax all edges (V-1) times
    for _ in range(num_currencies - 1):
        for src in range(num_currencies):
            for dest in range(num_currencies):
                if min_dist[dest] > min_dist[src] + rates_matrix.iloc[src, dest]:
                    min_dist[dest] = min_dist[src] + rates_matrix.iloc[src, dest]
                    predecessor[dest] = src

    # Check whether there are still 'relaxable' edges (which imply a negative cycle)
    opportunities = []
    for src in range(num_currencies):
        for dest in range(num_currencies):
            if min_dist[dest] > min_dist[src] + rates_matrix.iloc[src][dest] + log_margin:
                # negative cycle exists, and use the predecessor chain to print the cycle
                cycle = [dest]
                
                # Start from the source and go backwards until you see the source vertex again
                while True:
                    src = predecessor[src]
                    if src in cycle:
                        break
                    cycle.append(src)
                cycle.append(dest)
                
                if len(cycle) > 2:
                    path = [currencies[p] for p in cycle[::-1]]
                    if path not in opportunities:
                        opportunities.append(path)

    return opportunities


def test_arbitrage_profit(arbitrage_opportunities, exchange_rates):
    max_profit = 0 
    best_cycle = None

    for path in arbitrage_opportunities:
        cycle = path.copy()
        initial_balance = 10_000
        final_balance = initial_balance
        source_currency = cycle.pop(0)

        while cycle:
            dest_currency = cycle.pop(0)
            src_idx = currency_names.index(source_currency)
            dest_idx = currency_names.index(dest_currency)
            final_balance *= exchange_rates[src_idx][dest_idx]
            source_currency = dest_currency  # move to next currency

        profit = final_balance - initial_balance

        if profit > max_profit: 
            max_profit = profit
            best_cycle = path

    if best_cycle:
        print(f'Most profitable arbitrage opportunity ({max_profit:.2f} GBP gain): {" -> ".join(best_cycle)}')
    else:
        print("No arbitrage opportunity found.")

# Define exchange rate matrix from project 24 csc3025
currency_names = ["GBP", "EUR", "USD", "CAD"]
exchange_rates = [
    [1.0000, 1.1989, 1.2437, 1.7850],  # GBP -> GBP, EUR, USD, CAD
    [0.8341, 1.0000, 0.9913, 1.4888],  # EUR -> GBP, EUR, USD, CAD
    [0.8041, 1.0088, 1.0000, 1.4350],  # USD -> GBP, EUR, USD, CAD
    [0.5602, 0.6717, 0.6968, 1.0000]   # CAD -> GBP, EUR, USD, CAD
]

log_rates_matrix = convert_to_log_matrix(exchange_rates, currency_names)
arbitrage_opportunities = Bellman_Ford_Arbitrage(log_rates_matrix)

# Display results
if arbitrage_opportunities:
    test_arbitrage_profit(arbitrage_opportunities, exchange_rates)
else:
    print("No arbitrage opportunity.")