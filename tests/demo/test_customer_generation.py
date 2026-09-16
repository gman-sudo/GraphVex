from graphvex.synthetic.generator import generate_customers


customers = generate_customers(10)

for customer in customers:
    print(customer)