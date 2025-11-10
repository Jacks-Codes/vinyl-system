#!/bin/bash
# Setup audio routing: Turntable line-in -> Virtual sink -> AirPlay

echo "Creating virtual sink for vinyl output..."
pactl load-module module-null-sink sink_name=vinyl_out sink_properties=device.description="Vinyl-Output"

echo "Creating loopback: line-in -> vinyl_out..."
pactl load-module module-loopback source=alsa_input.pci-0000_00_1f.3.analog-stereo sink=vinyl_out latency_msec=1

echo "Setting vinyl input volume to 100%..."
pactl set-source-volume alsa_input.pci-0000_00_1f.3.analog-stereo 100%

echo "Audio routing configured!"
echo "Virtual sink: vinyl_out"
echo "Monitor source: vinyl_out.monitor"
pactl list sinks short | grep vinyl
