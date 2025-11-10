#!/usr/bin/env python3
"""
Stream live turntable audio to Apple TV
Uses a rolling buffer approach: capture audio chunks and stream them
"""
import asyncio
import sys
import subprocess
import tempfile
import os
from pathlib import Path
import pyatv

APPLETV_IP = "192.168.1.4"  # boys tv
AUDIO_SOURCE = "vinyl_out.monitor"
CHUNK_DURATION = 30  # seconds per chunk

async def capture_audio_chunk(output_file, duration=CHUNK_DURATION):
    """Capture audio chunk from turntable"""
    cmd = [
        'parec',
        f'--device={AUDIO_SOURCE}',
        '--format=s16le',
        '--rate=44100',
        '--channels=2'
    ]
    
    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-f', 's16le',
        '-ar', '44100',
        '-ac', '2',
        '-i', 'pipe:0',
        '-t', str(duration),
        '-acodec', 'aac',
        '-b:a', '256k',
        output_file
    ]
    
    # Pipe parec into ffmpeg
    parec_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=parec_proc.stdout, 
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    parec_proc.stdout.close()
    ffmpeg_proc.wait()
    parec_proc.terminate()

async def stream_to_appletv():
    """Main streaming loop"""
    print(f"Connecting to Apple TV at {APPLETV_IP}...")
    
    # Scan for Apple TV
    loop = asyncio.get_event_loop()
    atvs = await pyatv.scan(loop, hosts=[APPLETV_IP], timeout=5)
    
    if not atvs:
        print("❌ Apple TV not found!")
        return
    
    conf = atvs[0]
    print(f"✓ Found: {conf.name}")
    
    # Connect
    atv = await pyatv.connect(conf, loop)
    
    try:
        print(f"\n🎵 Streaming from turntable to {conf.name}")
        print("Press Ctrl+C to stop\n")
        
        chunk_num = 0
        temp_dir = tempfile.mkdtemp(prefix="vinyl_stream_")
        
        while True:
            chunk_file = os.path.join(temp_dir, f"chunk_{chunk_num}.m4a")
            
            print(f"[Chunk {chunk_num}] Capturing audio...")
            await capture_audio_chunk(chunk_file)
            
            print(f"[Chunk {chunk_num}] Streaming to Apple TV...")
            await atv.stream.stream_file(chunk_file)
            
            # Clean up old chunk
            if chunk_num > 0:
                old_file = os.path.join(temp_dir, f"chunk_{chunk_num-1}.m4a")
                if os.path.exists(old_file):
                    os.remove(old_file)
            
            chunk_num += 1
            
    except KeyboardInterrupt:
        print("\n\n⏹ Stopping stream...")
    finally:
        atv.close()
        # Cleanup temp files
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        print("✓ Cleaned up")

if __name__ == "__main__":
    try:
        asyncio.run(stream_to_appletv())
    except KeyboardInterrupt:
        pass
