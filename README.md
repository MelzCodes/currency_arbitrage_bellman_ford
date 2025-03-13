# Bellman Ford currency arbitrage detection algorithm

The Bellman Ford algorithm got famous for quickly solving the 'shortest path problem' on directed graphs. Particularly, it is useful in this case as oppose to an alogrithm like Djikstra's since it can handle negative weights.

It's application to currency trading is due to the fact that if there are still "relaxable edges" on a currency rates' matrix, then there is a negative cycle, which represents an arbitrage opportunity.

This repository contains a Python script to identify arbitrage opportunities in currency trading using the Bellman-Ford algorithm. The script takes a 2D list of current exchange rates and processes them to find profitable arbitrage cycles.

## Features

- Uses the Bellman-Ford algorithm to detect currency arbitrage opportunities.
- Outputs potential profitable currency trading paths.
- Live rates script pulls the top 10 currencies live prices and detects arbitrage opportunities in real time.

## Usage

1. **Clone the repository:**

```bash
   https://github.com/your-username/currency-arbitrage.git](https://github.com/MelzCodes/currency_arb_bellman_ford/blob/main/currency_arb_bellman_ford.py
```

2. **Install the required packages:**

```bash
  from math import log
  import pandas as pd
```

3. **For the Live rates script:**
   Install requests package

```bash
  import requests # (obs #1)
```

Create your API key:

```bash
   https://www.exchangerate-api.com/
```
