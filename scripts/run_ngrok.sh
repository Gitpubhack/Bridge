#!/bin/bash

# Bridge Exchange - Ngrok Setup Script
# This script starts ngrok and updates the configuration

echo "🚀 Starting ngrok for Bridge Exchange..."

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install it first:"
    echo "   - Download from https://ngrok.com/download"
    echo "   - Or install via package manager"
    exit 1
fi

# Check if port is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <port>"
    echo "Example: $0 8000"
    exit 1
fi

PORT=$1

echo "📡 Starting ngrok tunnel on port $PORT..."

# Start ngrok in background
ngrok http $PORT --log=stdout > ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

# Get the public URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnels = data.get('tunnels', [])
    for tunnel in tunnels:
        if tunnel.get('proto') == 'https':
            print(tunnel.get('public_url', ''))
            break
except:
    pass
")

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL"
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo "✅ Ngrok tunnel started successfully!"
echo "🌐 Public URL: $NGROK_URL"
echo "📋 Update your config.py with:"
echo "   NGROK_URL = \"$NGROK_URL\""
echo ""
echo "🔗 Telegram WebApp URL: $NGROK_URL/frontend/"
echo ""
echo "📝 To stop ngrok, run: kill $NGROK_PID"
echo "📄 Logs are saved in ngrok.log"

# Save the URL to a file for easy access
echo "$NGROK_URL" > ngrok_url.txt
echo "💾 URL saved to ngrok_url.txt"

# Keep the script running
echo "⏳ Press Ctrl+C to stop ngrok..."
wait $NGROK_PID
