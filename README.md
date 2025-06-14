# Pumpfun Wallets MCP

An MCP server that analyzes wallets’ trading activity and profitability on Pump.fun and PumpSwap.

![GitHub License](https://img.shields.io/github/license/kukapay/pumpfun-wallets-mcp) 
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Total Wallets**: Retrieve the total number of wallets on Pumpfun and Pumpswap.
- **Top Profitable Wallets**: Fetch the top wallets by realized profit over the last 30 days, with rank, wallet address, profit, and last transaction timestamp.
- **Top Trading Wallets**: Get the top wallets by all-time trading volume, including trade count and total volume in USD.
- **Wallet Distribution**: View the distribution of wallets by trading volume tiers, excluding bots, for insights into trading activity.
- **Tabulated Output**: Returns data in a clean, tabulated string format for easy readability.

## Prerequisites

- Python 3.10+
- A valid [Dune Analytics API key](https://dune.com/docs/api/#authentication)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/pumpfun-wallets-mcp.git
   cd pumpfun-wallets-mcp
   ```

2. **Install Dependencies**:
   ```bash
   uv sync
   ```

3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install main.py --name "pumpfun-wallets-mcp"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "Pumpfun Wallets": {
               "command": "uv",
               "args": [ "--directory", "/path/to/pumpfun-wallets-mcp", "run", "main.py" ],
               "env": { "DUNE_API_KEY": "dune_api_key"}               
           }
       }
    }
    ```
    Replace `/path/to/pumpfun-wallets-mcp` with your actual installation path, and `dune_api_key` with your API key from Dune Analytics.

    
## Tools

The server provides the following tools, accessible via the MCP interface or API:

### get_total_wallets()

- **Description**: Retrieves the total number of wallets on Pumpfun and Pumpswap.
- **Returns**: Integer (total wallet count, or 0 on error).
- **Example**:
```
How many wallets are there on Pumpfun and Pumpswap?
```

### get_alpha_wallets(limit: int = 100)

- **Description**: Fetches the top profitable wallets for the last 30 days, including rank, wallet address, realized profit (USD), and last transaction timestamp.
- **Parameters**: `limit` (optional, default: 100) - Maximum number of wallets to return.
- **Returns**: Tabulated string with wallet data, or empty string on error.
- **Example**:
```
Show me the top 5 most profitable wallets on Pumpfun and Pumpswap for the last 30 days.
```
Output:
```
Rank  Wallet                                      Realized Profit  Last Tx
----  ------------------------------------------  ---------------  --------------------
1     0x123...abc                                $50000           2025-06-10 12:34:56
2     0x456...def                                $45000           2025-06-09 09:12:34
...
```

### get_trading_wallets(limit: int = 10)

- **Description**: Retrieves the top wallets by all-time trading volume, including rank, wallet address, trade count, and total volume (USD).
- **Parameters**: `limit` (optional, default: 10) - Maximum number of wallets to return.
- **Returns**: Tabulated string with wallet data, or empty string on error.
- **Example**:
```
Who are the top 3 wallets with the highest trading volume on Pumpfun and Pumpswap?
```
Output:
```
Rank  Wallet                                      Trade Count  Total Volume
----  ------------------------------------------  -----------  ------------
1     0x789...ghi                                1500         $1000000
2     0xabc...jkl                                1200         $950000
3     0xdef...mno                                1000         $800000
```

### get_trading_wallet_distribution()

- **Description**: Fetches the distribution of wallets by trading volume tiers (excluding bots).
- **Returns**: Tabulated string with volume tiers and wallet counts, or empty string on error.
- **Example**:
```
What is the distribution of wallets by trading volume on Pumpfun and Pumpswap, excluding bots?
```
Output:
```
Volume Tier      Number of Wallets
---------------  -----------------
$0 - $1000       5000
$1000 - $10000   2000
$10000+          500
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

