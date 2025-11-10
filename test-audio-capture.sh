#!/bin/bash
# Test recording from turntable input

echo "Recording 5 seconds of audio from line-in..."
echo "Make sure turntable is playing!"
echo "Output file: test-capture.wav"

parec --device=alsa_input.pci-0000_00_1f.3.analog-stereo --format=s16le --rate=48000 --channels=2 | \
  ffmpeg -f s16le -ar 48000 -ac 2 -i pipe:0 -t 5 -y ~/vinyl-system/test-capture.wav

echo "Recording complete!"
echo "Play it back with: aplay ~/vinyl-system/test-capture.wav"
