#!/bin/bash
# Test streaming to Apple TV using ffmpeg

APPLETV_IP="192.168.1.4"
APPLETV_PORT="7000"

echo "Testing ffmpeg stream to Apple TV at $APPLETV_IP"
echo "Capturing from: vinyl_out.monitor"
echo "Press Ctrl+C to stop"
echo ""

# Stream using RTSP (Real Time Streaming Protocol)
parec --device=vinyl_out.monitor --format=s16le --rate=44100 --channels=2 | \
  ffmpeg -f s16le -ar 44100 -ac 2 -i pipe:0 \
    -acodec libmp3lame -b:a 320k \
    -f rtp rtp://$APPLETV_IP:$APPLETV_PORT

