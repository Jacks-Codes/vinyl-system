#!/usr/bin/env python3
"""
Stream audio from turntable (line-in) to HomePod via AirPlay
"""
import asyncio
import sys
from pyatv import scan

async def discover_devices():
    """Scan network for AirPlay devices"""
    print("Scanning for AirPlay devices...")
    loop = asyncio.get_event_loop()
    devices = await scan(loop, timeout=5)
    
    if not devices:
        print("No AirPlay devices found!")
        return []
    
    # Filter for devices with AirPlay support
    airplay_devices = [d for d in devices if d.services]
    
    print(f"\nFound {len(airplay_devices)} AirPlay device(s):")
    for i, device in enumerate(airplay_devices, 1):
        services = ", ".join([str(s.protocol) for s in device.services])
        print(f"  {i}. {device.name} - {device.address} [{services}]")
    
    return airplay_devices

async def main():
    devices = await discover_devices()
    if not devices:
        print("\nNo AirPlay devices found. Make sure HomePods are on the same network.")
        sys.exit(1)
    
    print("\n✓ Device discovery working!")
    print("\nNext step: Implement audio streaming")

if __name__ == "__main__":
    asyncio.run(main())
