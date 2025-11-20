// Configuration
const API_BASE_URL = 'http://localhost:4230';
const POLL_INTERVAL = 3000; // 3 seconds

// State Management
let currentRoom = null;
let currentPlayerName = null;
let isHost = false;
let pollInterval = null;

// DOM Elements
const screens = {
    landing: document.getElementById('landing-screen'),
    join: document.getElementById('join-screen'),
    waiting: document.getElementById('waiting-room-screen'),
    game: document.getElementById('game-screen')
};

const elements = {
    playerNameInput: document.getElementById('player-name'),
    createRoomBtn: document.getElementById('create-room-btn'),
    joinRoomBtn: document.getElementById('join-room-btn'),
    errorMessage: document.getElementById('error-message'),

    roomCodeInput: document.getElementById('room-code-input'),
    joinSubmitBtn: document.getElementById('join-submit-btn'),
    backFromJoinBtn: document.getElementById('back-from-join-btn'),
    joinErrorMessage: document.getElementById('join-error-message'),

    roomCodeDisplay: document.getElementById('room-code-display'),
    roomTitle: document.getElementById('room-title'),
    playerList: document.getElementById('player-list'),
    playerCount: document.getElementById('player-count'),
    maxPlayers: document.getElementById('max-players'),
    hostControls: document.getElementById('host-controls'),
    guestMessage: document.getElementById('guest-message'),
    startGameBtn: document.getElementById('start-game-btn'),
    leaveRoomBtn: document.getElementById('leave-room-btn'),
    waitingErrorMessage: document.getElementById('waiting-error-message'),

    backToLobbyBtn: document.getElementById('back-to-lobby-btn')
};

// Screen Management
function showScreen(screenName) {
    Object.values(screens).forEach(screen => screen.classList.remove('active'));
    screens[screenName].classList.add('active');
}

function showError(element, message) {
    element.textContent = message;
    element.classList.remove('hidden');
    setTimeout(() => element.classList.add('hidden'), 5000);
}

function clearError(element) {
    element.classList.add('hidden');
    element.textContent = '';
}

// API Calls
async function createRoom(hostName) {
    try {
        const response = await fetch(`${API_BASE_URL}/room/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                host_name: hostName,
                max_players: 10
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create room');
        }

        return await response.json();
    } catch (error) {
        console.error('Create room error:', error);
        throw error;
    }
}

async function joinRoom(roomCode, playerName) {
    try {
        const response = await fetch(`${API_BASE_URL}/room/join`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                room_code: roomCode,
                player_name: playerName
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to join room');
        }

        return await response.json();
    } catch (error) {
        console.error('Join room error:', error);
        throw error;
    }
}

async function getRoomInfo(roomCode) {
    try {
        const response = await fetch(`${API_BASE_URL}/room/${roomCode}`);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to get room info');
        }

        return await response.json();
    } catch (error) {
        console.error('Get room info error:', error);
        throw error;
    }
}

// Room Management
function startPolling() {
    stopPolling(); // Clear any existing interval
    pollInterval = setInterval(async () => {
        if (currentRoom) {
            try {
                const roomInfo = await getRoomInfo(currentRoom);
                updateWaitingRoom(roomInfo);
            } catch (error) {
                console.error('Polling error:', error);
                showError(elements.waitingErrorMessage, 'Lost connection to room');
                stopPolling();
            }
        }
    }, POLL_INTERVAL);
}

function stopPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
    }
}

function updateWaitingRoom(roomData) {
    // Update room code
    elements.roomCodeDisplay.textContent = roomData.room_code;
    elements.roomTitle.textContent = `Room ${roomData.room_code}`;

    // Update player count
    elements.playerCount.textContent = roomData.players.length;
    elements.maxPlayers.textContent = roomData.max_players;

    // Update player list
    elements.playerList.innerHTML = '';
    roomData.players.forEach(player => {
        const li = document.createElement('li');
        const isPlayerHost = player === roomData.host_name;

        if (isPlayerHost) {
            li.classList.add('player-host');
            li.innerHTML = `
                <span>${player}</span>
                <span class="host-badge">HOST</span>
            `;
        } else {
            li.innerHTML = `<span>${player}</span>`;
        }

        elements.playerList.appendChild(li);
    });

    // Show/hide host controls
    if (isHost) {
        elements.hostControls.classList.remove('hidden');
        elements.guestMessage.classList.add('hidden');
    } else {
        elements.hostControls.classList.add('hidden');
        elements.guestMessage.classList.remove('hidden');
    }
}

// Event Handlers
elements.createRoomBtn.addEventListener('click', async () => {
    const playerName = elements.playerNameInput.value.trim();

    if (!playerName) {
        showError(elements.errorMessage, 'Please enter your name');
        return;
    }

    clearError(elements.errorMessage);

    try {
        const roomData = await createRoom(playerName);

        currentRoom = roomData.room_code;
        currentPlayerName = playerName;
        isHost = true;

        // Fetch full room info and display
        const fullRoomData = await getRoomInfo(currentRoom);
        updateWaitingRoom(fullRoomData);

        showScreen('waiting');
        startPolling();
    } catch (error) {
        showError(elements.errorMessage, error.message);
    }
});

elements.joinRoomBtn.addEventListener('click', () => {
    const playerName = elements.playerNameInput.value.trim();

    if (!playerName) {
        showError(elements.errorMessage, 'Please enter your name');
        return;
    }

    currentPlayerName = playerName;
    showScreen('join');
});

elements.backFromJoinBtn.addEventListener('click', () => {
    clearError(elements.joinErrorMessage);
    elements.roomCodeInput.value = '';
    showScreen('landing');
});

elements.joinSubmitBtn.addEventListener('click', async () => {
    const roomCode = elements.roomCodeInput.value.trim();

    if (!roomCode || roomCode.length !== 6) {
        showError(elements.joinErrorMessage, 'Please enter a valid 6-digit room code');
        return;
    }

    clearError(elements.joinErrorMessage);

    try {
        const roomData = await joinRoom(roomCode, currentPlayerName);

        currentRoom = roomCode;
        isHost = false;

        // Fetch full room info and display
        const fullRoomData = await getRoomInfo(currentRoom);
        updateWaitingRoom(fullRoomData);

        showScreen('waiting');
        startPolling();
    } catch (error) {
        showError(elements.joinErrorMessage, error.message);
    }
});

elements.startGameBtn.addEventListener('click', () => {
    stopPolling();
    showScreen('game');
    // TODO: Implement actual game start logic
    console.log('Starting game for room:', currentRoom);
});

elements.leaveRoomBtn.addEventListener('click', () => {
    stopPolling();
    currentRoom = null;
    isHost = false;
    elements.playerNameInput.value = currentPlayerName;
    elements.roomCodeInput.value = '';
    clearError(elements.waitingErrorMessage);
    showScreen('landing');
});

elements.backToLobbyBtn.addEventListener('click', () => {
    showScreen('landing');
    currentRoom = null;
    currentPlayerName = null;
    isHost = false;
});

// Room code input validation (only numbers)
elements.roomCodeInput.addEventListener('input', (e) => {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
});

// Enter key support
elements.playerNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        elements.createRoomBtn.click();
    }
});

elements.roomCodeInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        elements.joinSubmitBtn.click();
    }
});

// Initialize
console.log('BALLPARK Game Client Initialized');
console.log('API Base URL:', API_BASE_URL);
