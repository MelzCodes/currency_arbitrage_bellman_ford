from math import log
import pandas as pd
from datetime import datetime

def create_currency_rates_df(rates_dict, currencies, neg_log=False):
    data = pd.DataFrame(index=currencies, columns=currencies)

    for currency in currencies:
        for currency_2 in currencies:
                data.loc[currency, currency_2] = rates_dict[currency][currency_2]

    data = data.astype(float)

    if neg_log:
        for currency_1 in currencies:
            for currency_2 in currencies:
                data.loc[currency_1, currency_2] = -log(data.loc[currency_1, currency_2])

    return data
    
def Bellman_Ford_Arbitrage(rates_matrix, log_margin = 0.001):
    currencies = rates_matrix.index    
    source = 0
    n = len(rates_matrix)
    min_dist = [float('inf')] * n

    # List of 'father-nodes'
    pre = [-1] * n
    min_dist[source] = 0

    # Relax all edges (V-1) times
    for _ in range(n-1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + rates_matrix.iloc[source_curr, dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + rates_matrix.iloc[source_curr, dest_curr]
                    pre[dest_curr] = source_curr

    # Test whether there are still 'relaxable' edges (which imply a negative cycle)
    opportunities = []
    for source_curr in range(n): # source_curr = 0
        for dest_curr in range(n): # dest_curr = 2
            if min_dist[dest_curr] > min_dist[source_curr] + rates_matrix.iloc[source_curr, dest_curr] + log_margin:
                # negative cycle exists, and use the predecessor chain to print the cycle
                cycle = [dest_curr]
                # Start from the source and go backwards until you see the source vertex again
                while True:
                    source_curr = pre[source_curr]
                    if source_curr in cycle:
                        break
                    cycle.append(source_curr)
                cycle.append(dest_curr)
                if len(cycle) > 3:
                    path = [currencies[p] for p in cycle]
                    if path not in opportunities:
                        opportunities.append(path)
    
    return opportunities

currencies = ['GBP', 'EUR', 'USD', 'CAD']
exchange_rates = [
    [1.0000, 1.1989, 1.2437, 1.7850],
    [0.8341, 1.0000, 1.0742, 1.4888],
    [0.8041, 1.0088, 1.0000, 1.4350],
    [0.5602, 0.6717, 0.6968, 1.0000]
]
exchange_dict = {
    currencies[i]: {
        currencies[j]: exchange_rates[i][j]
        for j in range(len(currencies))
    } for i in range(len(currencies))
}

rates = create_currency_rates_df(exchange_dict, currencies)
neg_log_rates = create_currency_rates_df(exchange_dict, currencies, neg_log = True)

print(f'Here are the FX-rates for Project 24:')
print(rates)

start = datetime.now()
arbitrage_opportunities = Bellman_Ford_Arbitrage(neg_log_rates)
if len(arbitrage_opportunities) > 0:
    print('\nEvaluate the gain of each opportunity:')

    # Testing
    for path in arbitrage_opportunities:
        arbitrage_1 = path.copy()    
        
        initial_balance = 10_000 # in the respective source-currency listed first on 'arbitrage_1'
        final_balance = initial_balance
        
        source_currency = arbitrage_1.pop()
        while arbitrage_1:
            dest_currency = arbitrage_1.pop()
            final_balance *= rates[source_currency][dest_currency]        
            source_currency = dest_currency
        
        if final_balance - initial_balance > 0.5:
            d = final_balance - initial_balance
            print(f'{path}: £{round(d, 2)} gain from £{initial_balance} investment')
        
        else:
            d = final_balance - initial_balance
            print(f'{path}: Not profitiable, £{round(d, 2)} gain from £{initial_balance} investment')

else:
    print('No arbitrage opportunity exists :(')

end = datetime.now()
print(f'\nTime taken to execute script: {end - start}')