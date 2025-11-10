#!/bin/bash
# Start streaming turntable audio to Apple TV

echo "========================================="
echo "  Vinyl → Apple TV Streaming"
echo "========================================="
echo ""

# Check if vinyl_out sink exists
if ! pactl list sinks short | grep -q vinyl_out; then
    echo "⚠ Audio routing not configured. Running setup..."
    ~/vinyl-system/setup-audio-routing.sh
    echo ""
fi

# Check audio levels
echo "Current line-in volume:"
pactl list sources | grep -A 10 "alsa_input.pci-0000_00_1f.3.analog-stereo" | grep Volume
echo ""

echo "Starting stream to Apple TV (boys tv)..."
echo "Make sure:"
echo "  ✓ Turntable is powered on"
echo "  ✓ Record is playing"
echo "  ✓ Apple TV is on and connected to HomePods"
echo ""
echo "Press Ctrl+C to stop streaming"
echo ""

cd ~/vinyl-system
source venv/bin/activate
python stream-live-to-appletv.py
