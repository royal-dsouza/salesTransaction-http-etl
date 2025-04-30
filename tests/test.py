import requests
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)


url = "http://localhost:8080"
payload = {
    "transaction_id": "TX12345",
    "product_id": "P001",
    "amount": 150.0,
    "customer_id": "CUST123"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
