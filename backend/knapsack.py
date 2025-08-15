from typing import List, Dict, Tuple

def knapsack(items: List[Dict], budget: int) -> Tuple[List[Dict], int, int]:
    """
    Solves the 0/1 Knapsack problem using dynamic programming.

    Args:
        items (List[Dict]): A list of items, each with 'name', 'price', and 'value'.
        budget (int): The maximum total cost allowed.

    Returns:
        Tuple:
            - List[Dict]: Selected items that maximize total value within budget.
            - int: Total price of selected items.
            - int: Total value of selected items.
    """
    n = len(items)

    if n == 0 or budget <= 0:
        return [], 0, 0

    # Initialize DP table with dimensions (n+1) x (budget+1)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Build table bottom-up
    for i in range(1, n + 1):
        item_price = items[i - 1]["price"]
        item_value = items[i - 1]["value"]

        for b in range(1, budget + 1):
            if item_price <= b:
                # Option to include or exclude the item
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - item_price] + item_value)
            else:
                # Cannot include this item
                dp[i][b] = dp[i - 1][b]

    # Backtrack to find which items were included
    selected_items = []
    b = budget

    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            selected_items.append(items[i - 1])
            b -= items[i - 1]["price"]

    selected_items.reverse()

    total_price = sum(item["price"] for item in selected_items)
    total_value = dp[n][budget]

    return selected_items, total_price, total_value
