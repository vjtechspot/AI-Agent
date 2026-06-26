import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv(".env")

# All duplicate trunk IDs from your dashboard
TRUNK_IDS = [
    "ST_2fFh3dYPxRvb",
    "ST_7umJ9KSCthVj", 
    "ST_x8ZM8o8W74Sv",
    "ST_FT8A79YVU5SU",
    "ST_PpLpJMNY4uXm",
    "ST_cUeQP2XcEP5i",
    "ST_wmkwNNgTjde7",
    "ST_iNBUz9SVJP4x",
    "ST_medNbtJj5U2G",
    "ST_qIpauhPqRS9o"
]

async def main():
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    if not (url and api_key and api_secret):
        print("❌ Missing LiveKit credentials in .env")
        return

    lkapi = api.LiveKitAPI(url=url, api_key=api_key, api_secret=api_secret)
    sip = lkapi.sip

    try:
        print("🗑️  Deleting all duplicate SIP trunks...")
        deleted_count = 0
        
        for trunk_id in TRUNK_IDS:
            try:
                print(f"   Deleting: {trunk_id}")
                await sip.delete_sip_trunk(trunk_id)
                print(f"   ✅ Deleted successfully")
                deleted_count += 1
            except Exception as e:
                print(f"   ❌ Failed to delete {trunk_id}: {e}")

        print(f"\n✅ Cleanup complete! Deleted {deleted_count} trunks.")
        print("   Now run: python create_trunk.py to create a fresh trunk")

    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(main())
