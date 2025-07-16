import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PANEL_API_URL = os.getenv("PANEL_API_URL", "https://electrosmm.com/adminapi/v1")
PANEL_API_KEY = os.getenv("PANEL_API_KEY")

# You must hardcode or pass the service ID (type) to use the admin API correctly
SERVICE_ID = os.getenv("SERVICE_ID", "1")  # Replace "1" with your real service ID

async def get_pending_order():
    payload = {
        "key": PANEL_API_KEY,
        "action": "getOrder",
        "type": SERVICE_ID
    }
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(PANEL_API_URL, data=payload)
            result = res.json()
            print("✅ Response:", result)
            return result
    except Exception as e:
        print("❌ Error:", e)
        return {"error": str(e)}
