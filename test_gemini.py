from decouple import config
import requests
from requests.exceptions import Timeout, RequestException

GEMINI_API_KEY = config('GEMINI_API_KEY')
print(f"API Key: {GEMINI_API_KEY[:20]}...")

# Using gemini-2.5-flash - the latest stable flash model
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

payload = {
    "contents": [{
        "parts": [{"text": "What is digital marketing?"}]
    }]
}

print("\n⏳ Sending request to Gemini API...")

try:
    # Increased timeout to 30 seconds
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print("\n✅ API is working!")
        # Parse and display the actual response
        data = response.json()
        if 'candidates' in data:
            text = data['candidates'][0]['content']['parts'][0]['text']
            print(f"\n📝 Generated Response:\n{text}")
        else:
            print(f"\nUnexpected response format: {data}")
    else:
        print(f"\n❌ API Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")

except Timeout:
    print("\n⏱️ Request timed out. This could be due to:")
    print("  - Slow internet connection")
    print("  - API server is slow to respond")
    print("  - Network issues")
    print("\n💡 Try running the script again or check your internet connection")

except RequestException as e:
    print(f"\n❌ Request failed: {str(e)}")
    print("Check your internet connection and try again")

except Exception as e:
    print(f"\n❌ Unexpected error: {str(e)}")