from django.test import TestCase
import requests

# Create your tests here.

print(requests.get("http://192.168.0.164:8020/all_categories").json())