from mcp.server.fastmcp import FastMCP
import httpx
import os
from dotenv import load_dotenv
import time
from tabulate import tabulate

# Load environment variables
load_dotenv()

# Initialize MCP server
mcp = FastMCP(
    name="Pump.fun Wallets",
    dependencies=["httpx", "pandas", "python-dotenv"]
)

# Configuration
DUNE_API_KEY = os.getenv("DUNE_API_KEY")
BASE_URL = "https://api.dune.com/api/v1"
HEADERS = {"X-Dune-API-Key": DUNE_API_KEY}

def get_latest_result(query_id: int, limit: int = 1000):
    """
    Fetch the latest results from a Dune Analytics query.

    Args:
        query_id (int): The ID of the Dune query to fetch results from.
        limit (int, optional): Maximum number of rows to return. Defaults to 1000.

    Returns:
        list: A list of dictionaries containing the query results, or an empty list if the request fails.

    Raises:
        httpx.HTTPStatusError: If the API request fails due to a client or server error.
    """
    url = f"{BASE_URL}/query/{query_id}/results"
    params = {"limit": limit}
    with httpx.Client() as client:
        response = client.get(url, params=params, headers=HEADERS, timeout=300)
        response.raise_for_status()
        data = response.json()
        
    result_data = data.get("result", {}).get("rows", [])
    return result_data

@mcp.tool()
def get_total_wallets() -> int:
    """
    Retrieve the total number of wallets on Pumpfun and Pumpswap platforms.

    This function queries Dune Analytics (query ID: 5239155) to fetch the total wallet count.

    Returns:
        int: The total number of wallets, or 0 if the query fails.

    Raises:
        Exception: If the API request or data retrieval encounters an error.
    """
    try:
        data = get_latest_result(5239155)
        return data[0].get("total_wallets", 0)
    except:
        return 0
    
@mcp.tool()
def get_alpha_wallets(limit: int = 100) -> str:
    """
    Retrieve the top profitable wallets on Pumpfun and Pumpswap for the last 30 days.

    This function queries Dune Analytics (query ID: 4032586) to fetch a ranked list of wallets
    based on their realized profit over the past 30 days, formatted as a tabulated string.

    Args:
        limit (int, optional): Maximum number of wallets to return. Defaults to 100.

    Returns:
        str: A tabulated string containing the rank, wallet address, realized profit (in USD),
             and last transaction timestamp for each wallet, or an empty string if the query fails.

    Raises:
        Exception: If the API request or data retrieval encounters an error.
    """
    try:
        data = get_latest_result(4032586, limit)
        rows = [
            [row["rank"], row["wallet"], f'${row["realized_profit"]:.0f}', row["last_tx"]]
            for row in data
        ]
        headers = ["Rank", "Wallet", "Realized Profit", "Last Tx"]
        return tabulate(rows, headers=headers)
    except:
        return ""
      
@mcp.tool()
def get_trading_wallets(limit: int = 10) -> str:
    """
    Retrieve the top wallets by all-time trading volume on Pumpfun and Pumpswap.

    This function queries Dune Analytics (query ID: 5232018) to fetch a ranked list of wallets
    based on their total trading volume, formatted as a tabulated string.

    Args:
        limit (int, optional): Maximum number of wallets to return. Defaults to 10.

    Returns:
        str: A tabulated string containing the rank, wallet address, trade count, and total
             trading volume (in USD) for each wallet, or an empty string if the query fails.

    Raises:
        Exception: If the API request or data retrieval encounters an error.
    """
    try:
        data = get_latest_result(5232018, limit)
        rows = [
            [row["rank"], row["wallet"], row["trade_count"], f'${row["total_volume_usd"]:.0f}']
            for row in data
        ]
        headers = ["Rank", "Wallet", "Trade Count", "Total Volume"]
        return tabulate(rows, headers=headers)
    except:
        return ""
      
@mcp.tool()
def get_trading_wallet_distribution() -> str:
    """
    Retrieve the distribution of wallets by trading volume on Pumpfun and Pumpswap, excluding bots.

    This function queries Dune Analytics (query ID: 5239138) to fetch the number of wallets
    grouped by trading volume tiers, formatted as a tabulated string.

    Returns:
        str: A tabulated string containing the volume tier and number of wallets in each tier,
             or an empty string if the query fails.

    Raises:
        Exception: If the API request or data retrieval encounters an error.
    """
    try:
        data = get_latest_result(5239138)
        rows = [
            [row["volume_tier"], row["num_wallets"]]
            for row in data
        ]
        headers = ["Volume Tier", "Number of Wallets"]
        return tabulate(rows, headers=headers)
    except:
        return ""

# Run the server
if __name__ == "__main__":
    mcp.run()