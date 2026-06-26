print("Testing imports...")
try:
    print("Importing livekit.agents...")
    import livekit.agents
    print("✅ livekit.agents OK")

    print("Importing livekit.api...")
    import livekit.api
    print("✅ livekit.api OK")

    print("Importing livekit.plugins.sarvam...")
    import livekit.plugins.sarvam
    print("✅ sarvam plugin OK")

    print("Importing livekit.plugins.deepgram...")
    import livekit.plugins.deepgram
    print("✅ deepgram plugin OK")

    print("Importing livekit.plugins.openai...")
    import livekit.plugins.openai
    print("✅ openai plugin OK")

    print("\nAll imports successful!")
except Exception as e:
    print(f"\n❌ ERROR during import: {e}")
except BaseException as be:
    print(f"\n❌ CRITICAL ERROR during import: {be}")
