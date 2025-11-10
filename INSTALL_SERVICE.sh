#!/bin/bash
# Install systemd service for auto audio routing

echo "Installing vinyl audio routing service..."

# Copy service file to user systemd directory
mkdir -p ~/.config/systemd/user/
cp ~/vinyl-system/vinyl-audio-routing.service ~/.config/systemd/user/

# Reload systemd
systemctl --user daemon-reload

# Enable service to start on login
systemctl --user enable vinyl-audio-routing.service

echo "✓ Service installed and enabled"
echo ""
echo "The audio routing will now automatically configure on login."
echo ""
echo "Manual control:"
echo "  Start:  systemctl --user start vinyl-audio-routing"
echo "  Stop:   systemctl --user stop vinyl-audio-routing"
echo "  Status: systemctl --user status vinyl-audio-routing"
