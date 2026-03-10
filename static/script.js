const messagesEl = document.getElementById('messages');
const inputEl    = document.getElementById('userInput');
const sendBtn    = document.getElementById('sendBtn');
const typingEl   = document.getElementById('typing');

const API_URL = 'http://127.0.0.1:8000';

function addMessage(text, role) {
  const row = document.createElement('div');
  row.className = `msg-row ${role}`;

  const label = document.createElement('span');
  label.className = 'msg-label';
  label.textContent = role === 'user' ? 'Me' : 'macha';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = text;

  row.appendChild(label);
  row.appendChild(bubble);

  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function send() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  inputEl.value = '';
  inputEl.disabled = true;
  sendBtn.disabled = true;

  typingEl.classList.add('active');
  messagesEl.scrollTop = messagesEl.scrollHeight;

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: text })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    typingEl.classList.remove('active');
    addMessage(data.answer, 'ai');
  } catch (error) {
    typingEl.classList.remove('active');
    addMessage(`Sorry, I encountered an error: ${error.message}`, 'ai');
    console.error('Chat error:', error);
  } finally {
    inputEl.disabled = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

sendBtn.addEventListener('click', send);
inputEl.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });

/* ── Easter Egg: Triple-Tap Detection ── */
let tapCount = 0;
let tapTimer = null;
const TAP_DELAY = 500;

const sparkleIcon = document.querySelector('.sparkle-icon');
const easterEggModal = document.getElementById('easterEggModal');
const closeEasterEgg = document.getElementById('closeEasterEgg');

if (sparkleIcon) {
  sparkleIcon.addEventListener('click', handleSparkleClick);
  sparkleIcon.style.cursor = 'pointer';
}

function handleSparkleClick() {
  tapCount++;

  if (tapCount === 1) {
    tapTimer = setTimeout(() => {
      tapCount = 0;
    }, TAP_DELAY);
  }

  if (tapCount === 3) {
    clearTimeout(tapTimer);
    tapCount = 0;
    showEasterEggModal();
  }
}

function showEasterEggModal() {
  if (easterEggModal) {
    easterEggModal.classList.add('show');
  }
}

function hideEasterEggModal() {
  if (easterEggModal) {
    easterEggModal.classList.remove('show');
  }
}

if (closeEasterEgg) {
  closeEasterEgg.addEventListener('click', hideEasterEggModal);
}

if (easterEggModal) {
  easterEggModal.addEventListener('click', (e) => {
    if (e.target === easterEggModal) {
      hideEasterEggModal();
    }
  });
}
