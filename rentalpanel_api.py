import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PANEL_API_URL = os.getenv("PANEL_API_URL", "https://yourpanel.com/adminapi/v1")
PANEL_API_KEY = os.getenv("PANEL_API_KEY")

async def get_order_status(order_id: str):
    payload = {
        "api_key": PANEL_API_KEY,
        "order_id": order_id
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{PANEL_API_URL}/order-status", json=payload)
            result = response.json()
            print("✅ API Response:", result)
            return result
    except Exception as e:
        print("❌ API Error:", e)
        return {"error": str(e)}
