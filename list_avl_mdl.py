from decouple import config
import requests

GEMINI_API_KEY = config('GEMINI_API_KEY')
print(f"API Key: {GEMINI_API_KEY[:20]}...")

# List all available models
list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

print("\n🔍 Fetching available models...\n")
response = requests.get(list_url, timeout=10)

if response.status_code == 200:
    data = response.json()
    print("✅ Available Models:\n")
    
    if 'models' in data:
        for model in data['models']:
            name = model.get('name', 'Unknown')
            display_name = model.get('displayName', 'Unknown')
            supported_methods = model.get('supportedGenerationMethods', [])
            
            print(f"Model: {name}")
            print(f"  Display Name: {display_name}")
            print(f"  Supported Methods: {', '.join(supported_methods)}")
            print()
    else:
        print("No models found in response")
        print(f"Response: {response.text}")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Response: {response.text}")