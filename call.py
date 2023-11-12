import requests

# response =  requests.get("http://127.0.0.1:8000/api/").json()
response = requests.patch("http://127.0.0.1:8000/api/mark_attendance/MOM?value=present&name=AMAN")
print(response)
