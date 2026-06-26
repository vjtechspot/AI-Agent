import sys
print(f"Python version: {sys.version}")

try:
    print("Testing 'import av' (Audio/Video library)...")
    import av
    print("✅ 'import av' successful")
except Exception as e:
    print(f"❌ 'import av' failed: {e}")

try:
    print("Testing 'import livekit.protocol'...")
    import livekit.protocol
    print("✅ 'import livekit.protocol' successful")
except Exception as e:
    print(f"❌ 'import livekit.protocol' failed: {e}")

try:
    print("Testing 'import livekit.agents'...")
    import livekit.agents
    print("✅ 'import livekit.agents' successful")
except Exception as e:
    print(f"❌ 'import livekit.agents' failed: {e}")
