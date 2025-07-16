import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PANEL_API_URL = os.getenv("PANEL_API_URL", "https://electrosmm.com/adminapi/v1")
PANEL_API_KEY = os.getenv("PANEL_API_KEY")

async def get_order_status(order_id: str):
    test_payloads = [
        {
            "key": PANEL_API_KEY,
            "action": "status",
            "order": order_id
        },
        {
            "key": PANEL_API_KEY,
            "action": "get_order",
            "order_id": order_id
        },
        {
            "key": PANEL_API_KEY,
            "action": "fetch_order_status",
            "id": order_id
        },
        {
            "key": PANEL_API_KEY,
            "action": "get_status",
            "id": order_id
        },
        {
            "key": PANEL_API_KEY,
            "action": "order",
            "id": order_id
        }
    ]

    for payload in test_payloads:
        print(f"🔍 Trying payload: {payload}")
        try:
            async with httpx.AsyncClient() as client:
                res = await client.post(PANEL_API_URL, data=payload)
                print("📦 Response:", res.text)
        except Exception as e:
            print("❌ Error:", e)

    return {"error": "None of the actions worked"}
