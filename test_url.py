import requests

print("Testing legit URL...")
res1 = requests.post("http://127.0.0.1:8000/analyze-url", json={"url": "chrome://newtab/"})
print(res1.json())

