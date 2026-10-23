# Mic transcript glitch

- Created: 2026-07-03T02:41:56Z
- Updated: 2026-07-06T11:52:37Z

---

## 🧑 You

Everything’s working pretty good except now on the phone of the only one I texted that when I use the microphone doesn’t torque back it writes a transcript

---

## 🤖 Kimi

Robust Microphone Component State Management Mobile Handling Transcript Control    The user is reporting a bug with a mobile interface where the microphone button doesn't "torque back" (return to its original state) after use, and instead writes a transcript. This is related to the Casa Companion project based on recent conversation history.Let me look at the context:Casa Companion is a frontend project with voice commandsThe user mentioned adding voice commands to charactersThe issue is specifically on mobile (phone) where the microphone button doesn't return to its original state after recording, and instead writes a transcriptThis sounds like a speech recognition / Web Speech API issue where:The microphone button doesn't visually reset after recording endsThe transcript is being written to the page instead of being processed as a commandI need to provide a fix for the microphone UI state management and transcript handling on mobile. Since this is a specific bug fix request and the user wants working code, I should provide the relevant JavaScript/CSS fix.Given the user's style (prefers direct script delivery, no long explanations), I should provide the fix immediately.The issue is likely:onresult handler is appending text directlyonend or onerror handler isn't resetting the microphone button stateMobile Safari/Chrome has different behavior for SpeechRecognition eventsI'll provide a robust microphone component fix that:Properly manages the UI state (recording/stopped)Handles the transcript correctly without writing it to the pageHandles mobile-specific quirks (SpeechRecognition can be flaky on mobile)Ensures the button returns to original stateSince I don't have the exact current code, I'll provide a complete, drop-in replacement for the microphone/voice command component that handles state properly.   Here’s the fix for the microphone state bug on mobile. Drop this into your voice command handler:JavaScript   Copy // === MOBILE MICROPHONE STATE FIX ===
class VoiceCommandController {
  constructor() {
    this.recognition = null;
    this.isListening = false;
    this.micButton = document.getElementById('mic-button'); // adjust selector
    this.transcriptBuffer = '';
    this.restartDelay = 300;
    this.init();
  }

  init() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      console.warn('Speech API not supported');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false; // mobile: single utterance per tap
    this.recognition.interimResults = false;
    this.recognition.lang = 'en-US';
    this.recognition.maxAlternatives = 1;

    this.bindEvents();
    this.bindButton();
  }

  bindEvents() {
    // Fires when speech is recognized
    this.recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript.trim().toLowerCase();
      this.transcriptBuffer = transcript;
      console.log('Voice input:', transcript);
      this.processCommand(transcript);
    };

    // CRITICAL: Reset UI on ANY end condition
    this.recognition.onend = () => {
      this.isListening = false;
      this.resetMicUI();
      // Auto-restart only if explicitly toggled (optional)
    };

    // Handle errors without breaking UI
    this.recognition.onerror = (event) => {
      console.error('Speech error:', event.error);
      this.isListening = false;
      this.resetMicUI();
      
      // Mobile-specific: no-speech often fires on short taps
      if (event.error === 'no-speech' || event.error === 'aborted') {
        this.showToast('No speech detected. Try again.');
      }
    };

    // Mobile Safari sometimes fires onstart late — force UI sync
    this.recognition.onstart = () => {
      this.isListening = true;
      this.setMicActive();
    };
  }

  bindButton() {
    if (!this.micButton) return;
    
    // Use pointer events for better mobile response
    this.micButton.addEventListener('pointerdown', (e) => {
      e.preventDefault(); // prevent zoom/scroll
      this.toggleMic();
    });

    // Prevent double-fire on some mobile browsers
    this.micButton.addEventListener('click', (e) => e.preventDefault());
  }

  toggleMic() {
    if (this.isListening) {
      this.stopListening();
    } else {
      this.startListening();
    }
  }

  startListening() {
    try {
      this.transcriptBuffer = '';
      this.recognition.start();
      // Optimistic UI update (in case onstart delays)
      this.setMicActive();
    } catch (err) {
      // Already started — reset and retry
      if (err.message?.includes('already started')) {
        this.recognition.stop();
        setTimeout(() => this.startListening(), this.restartDelay);
      }
    }
  }

  stopListening() {
    try {
      this.recognition.stop();
    } catch (e) {
      // Ignore stop errors
    }
    this.isListening = false;
    this.resetMicUI();
  }

  setMicActive() {
    if (!this.micButton) return;
    this.micButton.classList.add('mic-active', 'recording');
    this.micButton.classList.remove('mic-idle');
    this.micButton.setAttribute('aria-pressed', 'true');
    // Haptic feedback if available
    if (navigator.vibrate) navigator.vibrate(50);
  }

  resetMicUI() {
    if (!this.micButton) return;
    this.micButton.classList.remove('mic-active', 'recording');
    this.micButton.classList.add('mic-idle');
    this.micButton.setAttribute('aria-pressed', 'false');
  }

  processCommand(transcript) {
    // === YOUR COMMAND ROUTING HERE ===
    // Don't write to page — route to your character handlers
    const event = new CustomEvent('voicecommand', { 
      detail: { transcript, timestamp: Date.now() } 
    });
    document.dispatchEvent(event);
  }

  showToast(msg) {
    // Optional: flash message without breaking layout
    const toast = document.createElement('div');
    toast.className = 'voice-toast';
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
  }
}

// === CSS (add to your stylesheet) ===
/*
.mic-button {
  transition: transform 0.2s ease, background-color 0.2s ease;
  transform: scale(1);
  -webkit-tap-highlight-color: transparent; /* remove mobile tap flash */
}

.mic-button.recording {
  transform: scale(1.1);
  background-color: #ff4444; /* red recording state */
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.voice-toast {
  position: fixed;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 12px 24px;
  border-radius: 24px;
  font-size: 14px;
  z-index: 9999;
  pointer-events: none;
}
*/

// Init
const voice = new VoiceCommandController(); Key fixes for your bug:pointerdown + preventDefault() — stops the mobile browser from writing the transcript to the page or triggering zoom/scrollrecognition.continuous = false — mobile handles single utterances better; continuous mode often hangs the UIonend always resets UI — guarantees the button returns to idle even if speech is empty or errorsonerror catches no-speech — the most common mobile failure; prevents stuck "recording" stateNo transcript written to DOM — routes through CustomEvent instead so nothing leaks onto the pageIf your button selector is different, change document.getElementById('mic-button') to match your markup.                                                       Throw me a hard one. I'm ready.                       K2.6 Thinking

---
