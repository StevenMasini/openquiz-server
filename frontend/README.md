# BALLPARK - Landing Page

Simple, clean landing page for the BALLPARK competitive estimation game.

## Quick Start

### 1. Start the Backend Server

```bash
cd openquiz-server
pip install -r requirements.txt
python server.py
```

The server will start on `http://localhost:4230`

### 2. Open the Frontend

Simply open `index.html` in your web browser:

**Option A - Double Click:**
- Navigate to the `frontend` folder
- Double-click `index.html`

**Option B - From Browser:**
- Open your browser
- Press `Ctrl+O` (or `Cmd+O` on Mac)
- Navigate to `frontend/index.html` and open it

### 3. Test the App

**Create a Room:**
1. Enter your name
2. Click "CREATE ROOM"
3. You'll see a 6-digit room code
4. Share this code with friends

**Join a Room:**
1. Enter your name
2. Click "JOIN ROOM"
3. Enter the 6-digit code
4. Click "JOIN"

**Test with Multiple Players:**
1. Open the landing page in a normal browser window → Create a room
2. Open an incognito/private window → Join the room with the code
3. Both windows will show the player list updating automatically

## Features

- ✅ Create room with 6-digit codes
- ✅ Join existing rooms
- ✅ Real-time player list updates (polls every 3 seconds)
- ✅ Mobile-responsive design
- ✅ Clean, modern UI
- ✅ Error handling for all edge cases
- ✅ Host/guest role management

## Technical Details

**Frontend:**
- Pure HTML, CSS, JavaScript (no frameworks)
- Responsive design (works on mobile and desktop)
- Auto-polling for player list updates
- Fetch API for backend communication

**Backend:**
- Flask server on port 4230
- CORS enabled for browser access
- 30-minute room expiry
- Thread-safe room management
- Up to 10 players per room (configurable)

## API Endpoints Used

- `POST /room/create` - Create new room
- `POST /room/join` - Join existing room
- `GET /room/<code>` - Get room info (for polling)

## File Structure

```
frontend/
├── index.html       # Main landing page
├── css/
│   └── styles.css   # All styling
├── js/
│   └── app.js       # API logic and state management
└── README.md        # This file
```

## Next Steps

This is a foundation. Here's what you can add next:

1. **Game Logic** - Replace the placeholder "Game Starting..." screen with actual game
2. **WebSockets** - Replace polling with real-time WebSocket connections
3. **Room Settings** - Allow hosts to configure max players, game mode, etc.
4. **Player Avatars** - Add profile pictures or avatar selection
5. **Chat** - Add lobby chat functionality
6. **Sound Effects** - Add audio feedback for joins, starts, etc.
7. **Animations** - Add transitions between screens
8. **Disconnect Handling** - Handle players leaving/disconnecting gracefully

## Troubleshooting

**Can't connect to server:**
- Make sure the Flask server is running on port 4230
- Check console for CORS errors
- Verify the API_BASE_URL in `js/app.js` is correct

**Room codes not working:**
- Codes must be exactly 6 digits
- Codes expire after 30 minutes
- Server must be running

**Player list not updating:**
- Check browser console for errors
- Server must be running and accessible
- Polling happens every 3 seconds automatically

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Development Notes

**No Build Process Required:**
This is pure vanilla JavaScript - no Node.js, webpack, or build tools needed. Just open the HTML file in a browser.

**Easy to Migrate:**
This foundation can be easily migrated to React, Vue, or any framework later if needed.

**Production Ready:**
For production, you'll want to:
1. Host the frontend on a web server (not local files)
2. Use a production WSGI server for Flask
3. Add HTTPS
4. Add authentication
5. Add database persistence
6. Implement WebSockets
