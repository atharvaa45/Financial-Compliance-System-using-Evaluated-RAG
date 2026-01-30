import google.generativeai as genai
import os

# 1. SETUP: Replace with your actual API key
# Or set it in your terminal: export GEMINI_API_KEY="your_key"
api_key = "AIzaSyBXK-iDSBxZ6GeI0SXPZPuOHqc669dDe24"

genai.configure(api_key=api_key)

print("Fetching available models...\n")

try:
    # 2. LIST MODELS
    # We loop through all models and filter for those that can 'generateContent'
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Model Name: {m.name}")
            # print(f"   Display Name: {m.displayName}")
            print(f"   Description: {m.description}")
            print("-" * 40)

except Exception as e:
    print(f"❌ Error fetching models: {e}")