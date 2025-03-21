from math import log
import pandas as pd
import requests # (obs #1)
from datetime import datetime


def get_currency_rates(api_key, currencies, neg_log=False):
    data = pd.DataFrame(index = currencies, columns = currencies)
    for currency in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        rates = response.json()
        for currency_2 in currencies:
            if currency == currency_2:
                data.loc[currency, currency] = 1
            else:
                data.loc[currency, currency_2] = rates['conversion_rates'][currency_2]

    timestamp = rates['time_last_update_utc']
    if neg_log == False:
        data = data.astype(float)
        return data, timestamp
    else:
        for currency_1 in currencies: # currency_1 = currency
            for currency_2 in currencies:
                data.loc[currency_1, currency_2] = -log(data.loc[currency_1, currency_2])    
        return data, timestamp


def Bellman_Ford_Arbitrage(rates_matrix, log_margin = 0.001):
    currencies = rates_matrix.index    
    source = 0 # (obs #3)
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
            if min_dist[dest_curr] > min_dist[source_curr] + rates_matrix.iloc[source_curr, dest_curr] + log_margin: # (obs #2)
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
                    path = [currencies[p] for p in cycle[::-1]]
                    if path not in opportunities:
                        opportunities.append(path)
    
    return opportunities

api_key = 'you-cant-have-this-sorry'
top10_currencies = ['GBP', 'EUR', 'JPY', 'USD', 'CNY', 'AUD', 'CAD', 'CHF', 'HKD', 'SGD']\

start = datetime.now()
rates, rates_timestamp = get_currency_rates(api_key, top10_currencies)
end = datetime.now()
neg_log_rates, _ = get_currency_rates(api_key, top10_currencies, neg_log = True)

print(f'Here are the current rates at time: {rates_timestamp}\n')
print(rates)

print(f'\nTime taken to retrieve FX-rates from API: {end - start}')
start = datetime.now()
arbitrage_opportunities = Bellman_Ford_Arbitrage(neg_log_rates)
end = datetime.now()

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

print(f'\nTime taken to run algorithm: {end - start}')

'''_______________________________OBSERVATIONS___________________________________
obs #1: "Requests allows you to send HTTP/1.1 requests extremely easily. There's no need to 
manually add query strings to your URLs, or to form-encode your PUT & POST data — but 
nowadays, just use the json method!"

obs #2: 'log_margin' of 0.001 to avoid looking for insignificant arbitrage opportunities

obs #3: The Bellman-Ford algorithm can be run from any initial node
'''