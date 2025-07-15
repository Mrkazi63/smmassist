import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PANEL_API_URL = os.getenv("PANEL_API_URL", "https://yourpanel.com/api/v2")  # ← change this
PANEL_API_KEY = os.getenv("PANEL_API_KEY")

async def get_order_status(order_id: str):
    payload = {
        "key": PANEL_API_KEY,
        "action": "status",
        "order": order_id
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(PANEL_API_URL, data=payload)
        return response.json()
