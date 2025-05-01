import requests
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)


url = "http://localhost:8080"
payload = {
    "transaction_id": "TX123457",
    "product_id": "P009",
    "amount": 10.0,
    "customer_id": "CUST23"
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())
