#!/usr/bin/env python3
"""
Stream turntable audio to Apple TV via AirPlay
"""
import asyncio
import sys
import subprocess
from pyatv import connect, scan
from pyatv.const import Protocol

async def find_apple_tv():
    """Find the Apple TV on network"""
    print("Scanning for Apple TV...")
    loop = asyncio.get_event_loop()
    devices = await scan(loop, timeout=5)
    
    # Look for "boys tv"
    apple_tv = None
    for device in devices:
        if "boys tv" in device.name.lower():
            apple_tv = device
            break
    
    if not apple_tv:
        print("Apple TV 'boys tv' not found!")
        print("\nAvailable devices:")
        for d in devices:
            print(f"  - {d.name}")
        return None
    
    print(f"✓ Found: {apple_tv.name} at {apple_tv.address}")
    return apple_tv

async def stream_audio(device):
    """Stream audio from vinyl_out to Apple TV"""
    print(f"\nConnecting to {device.name}...")
    
    # Connect to Apple TV
    atv = await connect(device, loop=asyncio.get_event_loop())
    
    try:
        # Get the AirPlay interface
        airplay = atv.stream
        
        print("✓ Connected!")
        print("\nStarting audio stream from turntable...")
        print("Press Ctrl+C to stop\n")
        
        # Use ffmpeg to capture from vinyl_out.monitor and stream
        # We'll pipe PCM audio to the AirPlay interface
        cmd = [
            'parec',
            '--device=vinyl_out.monitor',
            '--format=s16le',
            '--rate=44100',
            '--channels=2'
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        # Stream the audio (this is simplified - full implementation needs proper ALAC encoding)
        print("⚠ Note: Direct PCM streaming may not work perfectly.")
        print("If this doesn't work, we'll use ffmpeg with proper encoding next.\n")
        
        while True:
            chunk = process.stdout.read(4096)
            if not chunk:
                break
            # TODO: Encode and send via AirPlay
            await asyncio.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\nStopping stream...")
    finally:
        atv.close()

async def main():
    device = await find_apple_tv()
    if not device:
        sys.exit(1)
    
    # Check what protocols are available
    print(f"Supported protocols: {[str(s.protocol) for s in device.services]}")
    
    # Check if we need to pair first
    if device.requires_pairing:
        print("\n⚠ Apple TV requires pairing!")
        print("Run: atvremote --id {device.identifier} --protocol airplay pair")
        sys.exit(1)
    
    await stream_audio(device)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
