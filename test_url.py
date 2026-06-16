import requests

print("Testing legit URL...")
res1 = requests.post("http://127.0.0.1:8000/api/analyze-url", json={"url": "https://github.com/prajwalvjois/some-repo"})
print(res1.json())

print("Testing phishing URL...")
res2 = requests.post("http://127.0.0.1:8000/api/analyze-url", json={"url": "http://paypal-security-login.example.com"})
print(res2.json())

print("Testing Email...")
res3 = requests.post("http://127.0.0.1:8000/api/analyze-email", json={"email_text": "Verify your paypal here: http://paypal-security-login.example.com"})
print(res3.json())
