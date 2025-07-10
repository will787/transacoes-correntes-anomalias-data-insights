import pandas as pd
from google import genai
from google.genai import types

from config import API_KEY

read_key = API_KEY

client = genai.Client(api_key=read_key)

response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents="whats the best way to analyze data for insights?", 
    config=types.GenerateContentConfig(system_instruction="You are specialist in topic of trade balance in brazil. " \
    "I will send to you informations about trade balance days, explain to me whats happening in this days"))


response = response.result