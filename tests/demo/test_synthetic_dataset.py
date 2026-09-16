from datetime import datetime

from graphvex.synthetic.generator import (
    generate_customers,
    generate_transactions,
)
from graphvex.synthetic.scenarios import (
    generate_structuring_scenario,
)


customers = generate_customers(100)

normal_transactions = generate_transactions(
    customers,
    1000,
)

structuring_transactions = generate_structuring_scenario(
    sender_id="C0012",
    receiver_ids=[
        "C0041",
        "C0072",
        "C0033",
        "C0058",
    ],
    start_time=datetime(2026, 1, 15, 10, 0),
)

transactions = normal_transactions + structuring_transactions

print("Normal transactions:", len(normal_transactions))
print("Structuring transactions:", len(structuring_transactions))
print("Total transactions:", len(transactions))

print("\nLast 4 transactions:")

for transaction in transactions[-4:]:
    print(transaction)