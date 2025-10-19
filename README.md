# Sylvia - Synctrack AI Voice Agent 🤖🎙️

**Sylvia** is Synctrack's intelligent voice AI agent that engages website visitors in natural conversations, explains automation services, and captures qualified leads directly into your CRM—all powered by your custom cloned voice.

Built with **LiveKit Agents Framework** + **ElevenLabs Voice Cloning** + **OpenAI GPT-4** + **Deepgram STT**

[![LiveKit](https://img.shields.io/badge/LiveKit-Agents-blue)](https://livekit.io)
[![ElevenLabs](https://img.shields.io/badge/ElevenLabs-Voice%20Cloning-green)](https://elevenlabs.io)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)](https://python.org)

---

## 📋 Table of Contents

- [What Sylvia Does](#-what-sylvia-does)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Local Testing](#-local-testing)
- [Deployment](#-deployment)
- [LiveKit Playground](#-livekit-playground)
- [Conversation Flow](#-conversation-flow)
- [Function Tools](#-function-tools)
- [CRM Integration](#-crm-integration)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Resources](#-resources)

---

## 🎯 What Sylvia Does

Sylvia is your 24/7 AI automation consultant that:

- **Engages naturally** with warm, conversational AI using your cloned voice
- **Explains Synctrack services** (automation, lead gen, AI workflows, voice agents, websites)
- **Qualifies leads** by understanding business needs and pain points
- **Captures data automatically** into n8n CRM via webhook
- **Available 24/7** for website visitors across multiple channels
- **Sounds like you** with ElevenLabs voice cloning technology

---

## ✨ Features

### Sylvia's Personality
- **Role**: Friendly, confident AI automation consultant
- **Tone**: Warm, helpful, professional (smart colleague, not a robot)
- **Style**: Natural speech with fillers ("hm", "sure thing", "makes sense")
- **Behavior**: Empathetic listener, asks thoughtful follow-up questions
- **Voice**: Custom cloned voice using ElevenLabs (sounds natural and human)

### Core Capabilities
- **Natural Language Understanding**: Powered by GPT-4o-mini for intelligent conversations
- **High-Accuracy Speech Recognition**: Deepgram Nova-2 for real-time transcription
- **Custom Voice Synthesis**: ElevenLabs cloned voice for authentic brand representation
- **Voice Activity Detection**: Silero VAD for natural turn-taking
- **Lead Qualification**: Automatically extracts and validates contact information
- **CRM Integration**: Direct webhook integration with n8n for instant lead capture

---

## 🔧 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | LiveKit Agents v1.2.15 | Voice AI orchestration |
| **STT** | Deepgram Nova-2 | Speech-to-text with 98% accuracy |
| **LLM** | OpenAI GPT-4o-mini | Natural language processing |
| **TTS** | ElevenLabs (Cloned Voice) | Text-to-speech with your voice |
| **VAD** | Silero VAD | Voice activity detection |
| **CRM** | n8n Webhook | Lead management |
| **Package Manager** | UV | Fast Python dependency management |

### 🎯 How It All Works Together: The Voice Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                    SYLVIA'S VOICE PIPELINE                        │
└──────────────────────────────────────────────────────────────────┘

1️⃣  User speaks: "I need help with automation"
                    ↓
2️⃣  🎤 Microphone captures audio
                    ↓
3️⃣  📝 DEEPGRAM (STT)
    Converts speech → text: "I need help with automation"
                    ↓
4️⃣  🧠 GPT-4o-mini (LLM)
    - Understands intent
    - Generates response
    - Calls function tools if needed (CRM, services, time)
    - Creates response text
                    ↓
5️⃣  🗣️ ELEVENLABS (TTS)
    Converts text → speech using YOUR cloned voice
                    ↓
6️⃣  🔊 Speakers play Sylvia's response
                    ↓
7️⃣  User hears: "That makes sense! Tell me about your current process..."

┌──────────────────────────────────────────────────────────────────┐
│  SILERO VAD detects when user starts/stops speaking for natural  │
│  turn-taking (prevents interruptions & awkward pauses)            │
└──────────────────────────────────────────────────────────────────┘
```

**In Simple Terms:**
- **Deepgram** = Sylvia's "ears" (hears what you say)
- **GPT-4o-mini** = Sylvia's "brain" (thinks and decides what to say)
- **ElevenLabs** = Sylvia's "voice" (speaks with your cloned voice)
- **Silero VAD** = Sylvia's "politeness" (knows when to listen vs speak)
- **LiveKit** = The "stage" that brings it all together

### 📊 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SYLVIA - COMPLETE SYSTEM FLOW                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   WEBSITE    │  User clicks "Talk to Sylvia" button
│   VISITOR    │  or calls phone number
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        LIVEKIT AGENTS (Cloud)                             │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                    SYLVIA'S BRAIN (sylvia_agent.py)                │  │
│  │                                                                    │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │  LISTENING STATE                                          │    │  │
│  │  │  ┌────────────┐                                          │    │  │
│  │  │  │ Silero VAD │ ◄─── Detects voice activity             │    │  │
│  │  │  └────────────┘                                          │    │  │
│  │  └──────────────┬───────────────────────────────────────────┘    │  │
│  │                 │                                                 │  │
│  │                 ▼                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │  SPEECH-TO-TEXT (STT)                                    │    │  │
│  │  │  ┌──────────────────────────────────────┐                │    │  │
│  │  │  │   🎤 Audio Stream                     │                │    │  │
│  │  │  │        ↓                              │                │    │  │
│  │  │  │   📝 DEEPGRAM NOVA-2                  │                │    │  │
│  │  │  │   Converts: Speech → Text             │                │    │  │
│  │  │  │   "I need automation for my business" │                │    │  │
│  │  │  └──────────────────────────────────────┘                │    │  │
│  │  └──────────────┬───────────────────────────────────────────┘    │  │
│  │                 │                                                 │  │
│  │                 ▼                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │  THINKING STATE                                          │    │  │
│  │  │  ┌──────────────────────────────────────┐                │    │  │
│  │  │  │   🧠 OPENAI GPT-4o-mini                │                │    │  │
│  │  │  │                                       │                │    │  │
│  │  │  │   1. Analyzes user intent             │                │    │  │
│  │  │  │   2. Retrieves context from memory    │                │    │  │
│  │  │  │   3. Decides if function call needed: │                │    │  │
│  │  │  │      ├─ send_to_crm()                 │                │    │  │
│  │  │  │      ├─ get_synctrack_services()      │                │    │  │
│  │  │  │      └─ get_current_time()            │                │    │  │
│  │  │  │   4. Generates natural response text  │                │    │  │
│  │  │  │                                       │                │    │  │
│  │  │  │   Output: "That makes sense! Let me  │                │    │  │
│  │  │  │   tell you about our automation..."   │                │    │  │
│  │  │  └──────────────────────────────────────┘                │    │  │
│  │  └──────────────┬───────────────────────────────────────────┘    │  │
│  │                 │                                                 │  │
│  │                 ├─────────────────┐                               │  │
│  │                 │                 │ (If lead qualified)           │  │
│  │                 │                 ▼                               │  │
│  │                 │    ┌────────────────────────────┐               │  │
│  │                 │    │   📊 FUNCTION: send_to_crm │               │  │
│  │                 │    └────────────┬───────────────┘               │  │
│  │                 │                 │                               │  │
│  │                 │                 ▼                               │  │
│  │                 │    ┌─────────────────────────────────────┐     │  │
│  │                 │    │  WEBHOOK POST to n8n CRM            │     │  │
│  │                 │    │  {                                  │     │  │
│  │                 │    │    "source": "voice",               │     │  │
│  │                 │    │    "name": "John Doe",              │     │  │
│  │                 │    │    "company": "Acme Corp",          │     │  │
│  │                 │    │    "intent": "automation",          │     │  │
│  │                 │    │    "email": "john@acme.com"         │     │  │
│  │                 │    │  }                                  │     │  │
│  │                 │    └─────────────────────────────────────┘     │  │
│  │                 │                                                 │  │
│  │                 ▼                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │  TEXT-TO-SPEECH (TTS)                                    │    │  │
│  │  │  ┌──────────────────────────────────────┐                │    │  │
│  │  │  │   🗣️ ELEVENLABS                       │                │    │  │
│  │  │  │   Voice ID: 6X0hgJwbuR7bBAFf3Krh     │                │    │  │
│  │  │  │                                       │                │    │  │
│  │  │  │   Converts: Text → Speech             │                │    │  │
│  │  │  │   Uses YOUR cloned voice              │                │    │  │
│  │  │  │                                       │                │    │  │
│  │  │  │   Output: 🎵 Audio stream             │                │    │  │
│  │  │  └──────────────────────────────────────┘                │    │  │
│  │  └──────────────┬───────────────────────────────────────────┘    │  │
│  │                 │                                                 │  │
│  │                 ▼                                                 │  │
│  │  ┌──────────────────────────────────────────────────────────┐    │  │
│  │  │  SPEAKING STATE                                          │    │  │
│  │  │  🔊 Audio plays to user                                   │    │  │
│  │  │  Silero VAD monitors for interruptions                    │    │  │
│  │  └──────────────────────────────────────────────────────────┘    │  │
│  │                                                                    │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  AGENT MEMORY (maintains conversation context)                │  │
│  │  - User name, company, email                                  │  │
│  │  - Conversation history                                       │  │
│  │  - Lead qualification status                                  │  │
│  └────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                      │
│                                                               │
│  ┌────────────────────┐         ┌──────────────────────┐     │
│  │  n8n CRM           │         │  LiveKit Playground  │     │
│  │  (Railway)         │         │  agents-playground   │     │
│  │                    │         │  .livekit.io         │     │
│  │  Receives leads    │         │                      │     │
│  │  Triggers workflows│         │  Testing interface   │     │
│  │  Sends to sales    │         │  for developers      │     │
│  └────────────────────┘         └──────────────────────┘     │
│                                                               │
│  ┌────────────────────┐         ┌──────────────────────┐     │
│  │  Website Widget    │         │  Phone Number        │     │
│  │  (Future)          │         │  (Optional)          │     │
│  │                    │         │                      │     │
│  │  Embed Sylvia      │         │  Twilio/LiveKit SIP  │     │
│  │  on your site      │         │  for phone calls     │     │
│  └────────────────────┘         └──────────────────────┘     │
└──────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                     STATE TRANSITION DIAGRAM                         │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  START   │
    └────┬─────┘
         │
         ▼
    ┌─────────────────┐
    │   LISTENING     │ ◄──────────────┐
    │  (Waiting for   │                │
    │   user speech)  │                │
    └────┬────────────┘                │
         │                             │
         │ User starts speaking        │
         ▼                             │
    ┌─────────────────┐                │
    │   THINKING      │                │
    │  (Processing    │                │
    │   with GPT-4)   │                │
    └────┬────────────┘                │
         │                             │
         │ Response generated          │
         ▼                             │
    ┌─────────────────┐                │
    │   SPEAKING      │                │
    │  (Sylvia talks  │                │
    │   with ElevenLabs)               │
    └────┬────────────┘                │
         │                             │
         │ Response complete           │
         └─────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────┐
│                    DATA FLOW FOR LEAD CAPTURE                        │
└─────────────────────────────────────────────────────────────────────┘

Conversation → GPT-4 extracts → Lead Data Object → send_to_crm() → n8n
                                      │
                                      ├─ Name: "John Doe"
                                      ├─ Company: "Acme Corp"
                                      ├─ Email: "john@acme.com"
                                      ├─ Phone: "+1234567890"
                                      ├─ Intent: "automation"
                                      └─ Summary: "Needs lead gen..."
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- [UV package manager](https://github.com/astral-sh/uv) (for dependency management)
- API Keys:
  - OpenAI API key ([Get it here](https://platform.openai.com/api-keys))
  - Deepgram API key ([Get it here](https://console.deepgram.com))
  - ElevenLabs API key ([Get it here](https://elevenlabs.io/app/settings/api-keys))
  - LiveKit Cloud account ([Sign up here](https://cloud.livekit.io))

### 1. Install Dependencies

```bash
cd "Synctrack voice agent"
uv sync
```

This will install all required packages:
- `livekit-agents[mcp]>=1.2.0`
- `livekit-plugins-openai>=1.0.0`
- `livekit-plugins-deepgram>=1.0.0`
- `livekit-plugins-silero>=1.0.0`
- `livekit-plugins-elevenlabs>=1.2.15`
- `python-dotenv>=1.0.0`
- `httpx>=0.25.0`

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# LiveKit Configuration (from cloud.livekit.io)
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# OpenAI Configuration (from platform.openai.com)
OPENAI_API_KEY=sk-proj-...

# Deepgram Configuration (from console.deepgram.com)
DEEPGRAM_API_KEY=your_deepgram_key

# ElevenLabs Configuration (from elevenlabs.io)
ELEVEN_API_KEY=sk_...
ELEVENLABS_API_KEY=sk_...  # Backup for compatibility
ELEVENLABS_VOICE_ID=your_cloned_voice_id

# Model Selection (Optional)
LLM_CHOICE=gpt-4o-mini

# Development Settings (Optional)
LOG_LEVEL=INFO
DEBUG_MODE=false
```

**Important**: Make sure your ElevenLabs API key has **full permissions** (including `voices_read`, `tts`, etc.)

### 3. Get Your ElevenLabs Voice ID

1. Go to [ElevenLabs Voice Library](https://elevenlabs.io/app/voice-library)
2. Clone your voice or select an existing voice
3. Copy the Voice ID
4. Add it to your `.env` file as `ELEVENLABS_VOICE_ID`

---

## 🧪 Local Testing

### Console Mode (Test with Microphone)

```bash
uv run python sylvia_agent.py console
```

This will:
1. Start Sylvia in console mode
2. Use your computer's microphone
3. Play responses through your speakers
4. Show real-time transcripts and state changes

**Expected Output:**
```
INFO:livekit.agents:starting worker
INFO:__main__:Sylvia started in room: mock_room
INFO:__main__:Sylvia session started
INFO:__main__:Sylvia state: listening -> thinking
INFO:__main__:Sylvia state: thinking -> speaking
```

**Interaction:**
- Sylvia will greet you: "Hey there! I'm Sylvia from Synctrack — how's your day going so far?"
- Talk naturally about your business needs
- She'll ask qualifying questions and explain relevant services
- Press `Ctrl+C` to exit

### Testing Tips

1. **Test the greeting**: Verify Sylvia speaks with your cloned voice
2. **Test lead capture**: Provide your name, company, email to test CRM integration
3. **Test service knowledge**: Ask about automation, AI agents, websites, etc.
4. **Test function calling**: Ask "what services does Synctrack offer?" or "what time is it?"

---

## 🚀 Deployment

### Option 1: Deploy to LiveKit Cloud (Recommended)

#### Step 1: Install LiveKit CLI

**Mac:**
```bash
brew install livekit-cli
```

**Windows:**
```bash
winget install LiveKit.LiveKitCLI
```

**Linux:**
```bash
curl -sSL https://get.livekit.io/cli | bash
```

#### Step 2: Authenticate

```bash
lk cloud auth
```

This will:
- Open your browser
- Ask you to sign in to LiveKit Cloud
- Save authentication credentials locally

#### Step 3: Create and Deploy Agent

```bash
cd "Synctrack voice agent"
lk agent create --secrets-file .env
```

You'll be prompted to:
1. **Enter agent name**: Type `sylvia`
2. **Confirm files**: Press Enter to upload all files
3. **Confirm secrets**: Press Enter to upload `.env` variables

The CLI will:
- Package your code
- Upload environment variables securely
- Build the agent Docker image
- Deploy to LiveKit Cloud
- Return deployment URL and status

**Expected Output:**
```
✓ Agent created successfully
✓ Building agent...
✓ Deploying agent...
✓ Agent deployed to: https://synctrack-xxxxx.livekit.cloud
```

#### Step 4: Verify Deployment

```bash
# List all agents
lk agent list

# Check agent status
lk agent status sylvia

# View logs
lk agent logs sylvia
```

### Updating an Existing Agent

If you've already deployed Sylvia and need to update the code (e.g., changing webhook endpoint, personality, or adding features):

#### Option 1: Update Command (Recommended)

```bash
cd "Synctrack voice agent"
lk agent update sylvia --secrets-file .env
```

This will:
- Update the existing agent without creating a new one
- Refresh all environment variables from `.env`
- Deploy your latest code changes
- Preserve your agent ID and configuration

**Use this when:**
- You've updated `sylvia_agent.py`
- You've changed webhook URLs
- You've modified `.env` variables
- You've added new function tools

#### Option 2: Delete and Recreate

If you hit the agent limit (e.g., "maximum number of agents reached"):

```bash
# Delete the old agent
lk agent delete sylvia

# Create new agent
lk agent create --secrets-file .env
```

**Important**: This will create a new agent ID. Use the update command instead when possible.

#### Verify Update

After updating, check the deployment:

```bash
# Check if update succeeded
lk agent status sylvia

# View recent logs to verify changes
lk agent logs sylvia --tail 50

# Test in playground
# Go to https://agents-playground.livekit.io/
```

---

## 🎮 LiveKit Playground

### Access the Playground

Once deployed, test Sylvia in the LiveKit Agents Playground:

**URL**: https://agents-playground.livekit.io/

### How to Use the Playground

#### 1. **Sign In**
   - Use your LiveKit Cloud credentials
   - Select your organization/project

#### 2. **Connect to Sylvia**
   - From the dropdown, select `sylvia` agent
   - Click **"Connect"** button
   - Allow microphone access when prompted

#### 3. **Start Talking**
   - The playground will show:
     - **Your transcript** (what you're saying)
     - **Sylvia's transcript** (what she's saying)
     - **State changes** (listening → thinking → speaking)
   - Speak naturally and wait for Sylvia to respond

#### 4. **Test Features**

**Test Greeting:**
- Connect and wait for Sylvia's greeting
- Verify: "Hey there! I'm Sylvia from Synctrack — how's your day going so far?"

**Test Service Knowledge:**
- Ask: "What services does Synctrack offer?"
- Sylvia should list: AI lead generation, workflow automation, voice AI agents, websites, CRM automation

**Test Lead Capture:**
- Provide your information naturally in conversation
- Say something like: "I'm John from Acme Corp, interested in automation"
- Sylvia will collect: name, company, email/phone, intent
- Check your n8n webhook for the lead data

**Test Function Tools:**
- Ask: "What time is it?" → Tests `get_current_time()`
- Ask: "Tell me about your services" → Tests `get_synctrack_services()`

#### 5. **Monitor Performance**

The playground shows:
- **Latency**: Time to first response
- **Audio Quality**: Voice clarity and naturalness
- **Turn-taking**: How well Sylvia handles interruptions
- **Transcript Accuracy**: How well speech is recognized

---

## 🎤 Conversation Flow

### 1. Warm Greeting
```
Sylvia: "Hey there! I'm Sylvia from Synctrack — how's your day going so far?"
```

### 2. Discovery Phase
- Sylvia asks about their business
- Listens actively to pain points
- Shows empathy and understanding
- Explains relevant Synctrack services

Example exchange:
```
User: "I'm looking to automate my lead generation process"
Sylvia: "That makes sense! Lead generation can be really time-consuming when done manually.
         At Synctrack, we build AI-powered lead generation systems that capture and qualify
         leads automatically. Can you tell me a bit about your current process?"
```

### 3. Lead Qualification
Sylvia naturally collects:
- Name
- Company
- Email address (optional)
- Phone number (optional)
- Main pain point / interest
- Brief conversation summary

### 4. CRM Capture
```
Sylvia: "Perfect! I've sent your information to our team. Someone from Synctrack will
         follow up soon to show you exactly how we can help [Company] with [Intent].
         Thanks for chatting with me today!"
```

The lead is instantly sent to your n8n Data Tables via webhook.

---

## 🛠️ Function Tools

Sylvia has three function tools that she can call autonomously:

### 1. `send_to_crm()`
Captures qualified lead information to n8n CRM

**Parameters:**
- `name` (str): Lead's full name
- `company` (str): Lead's company name
- `intent` (str): Main interest or pain point
- `email` (str, optional): Lead's email address
- `phone` (str, optional): Lead's phone number
- `summary` (str, optional): Brief conversation summary

**Returns:**
- Confirmation message for Sylvia to speak

**Example Call:**
```python
await send_to_crm(
    name="John Doe",
    company="Acme Corp",
    intent="lead generation automation",
    email="john@acme.com",
    phone="+1234567890",
    summary="Looking to automate lead capture process"
)
```

### 2. `get_synctrack_services()`
Returns detailed information about Synctrack's service offerings

**Parameters:** None

**Returns:**
- Formatted list of services with descriptions

**Services Included:**
1. AI Lead Generation Systems
2. Workflow Automation
3. Voice AI Agents
4. Modern Website Development
5. CRM & Reporting Automation

### 3. `get_current_time()`
Gets the current date and time

**Parameters:** None

**Returns:**
- Formatted timestamp string (e.g., "October 17, 2025 at 05:30 PM")

---

## 📊 CRM Integration

### Webhook Configuration

Sylvia automatically sends qualified lead data to your n8n CRM via webhook.

**Configure Your Webhook URL:**

1. **In `sylvia_agent.py` (line 29)**, update the webhook URL:
   ```python
   CRM_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/sylvia-voice-agent"
   ```

2. **Example n8n webhook URLs:**
   - n8n Cloud: `https://your-instance.app.n8n.cloud/webhook/sylvia-voice-agent`
   - Self-hosted: `https://n8n.yourdomain.com/webhook/sylvia-voice-agent`
   ```

### Payload Format

```json
{
  "source": "voice",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Acme Corp",
  "intent": "lead generation automation",
  "summary": "Looking to automate lead capture process. Currently using manual spreadsheets.",
  "timestamp": "2025-10-17T12:00:00Z"
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | string | ✅ | Always "voice" for Sylvia leads |
| `name` | string | ✅ | Lead's full name |
| `company` | string | ✅ | Lead's company name |
| `intent` | string | ✅ | Main interest or pain point |
| `email` | string | 🎯 | Lead's email (PRIORITY - highly recommended) |
| `phone` | string | ⭐ | Lead's phone (optional, but nice to have) |
| `summary` | string | ⭐ | Brief conversation summary (optional) |
| `timestamp` | string | ✅ | ISO 8601 timestamp (UTC) |

**Lead Capture Priority:**
- **MINIMUM REQUIRED**: name, company, intent
- **HIGHLY RECOMMENDED**: email (Sylvia will try to convince users to share it)
- **OPTIONAL**: phone number (bonus if provided)

### Setting Up Your n8n Webhook

**Step 1: Create Webhook in n8n**
1. Open your n8n workflow editor
2. Add a **Webhook** node (Trigger)
3. Set HTTP Method to `POST`
4. Set Path to `/webhook/sylvia-voice-agent`
5. Copy the webhook URL (it will look like: `https://your-n8n.com/webhook/sylvia-voice-agent`)

**Step 2: Update Sylvia's Configuration**
1. Open `sylvia_agent.py`
2. Find line 29: `CRM_WEBHOOK_URL = "..."`
3. Replace with your n8n webhook URL
4. Redeploy: `lk agent update sylvia --secrets-file .env`

**Step 3: Test Your Webhook**

Replace `YOUR_WEBHOOK_URL` with your actual webhook:

```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "source": "voice",
    "name": "Test Lead",
    "email": "test@example.com",
    "phone": "+1234567890",
    "company": "Test Corp",
    "intent": "testing webhook",
    "summary": "This is a test",
    "timestamp": "2025-10-17T12:00:00Z"
  }'
```

**Expected Response:** `200 OK` or `202 Accepted`

---

## ⚙️ Configuration

### Voice Pipeline Settings

Located in `sylvia_agent.py:215-241`

```python
session = AgentSession(
    # Speech-to-Text - Deepgram for high accuracy
    stt=deepgram.STT(
        model="nova-2",
        language="en-US",
    ),

    # Large Language Model - GPT-4o-mini for natural conversations
    llm=openai.LLM(
        model=os.getenv("LLM_CHOICE", "gpt-4o-mini"),
        temperature=0.8,  # Higher temp for more natural responses
    ),

    # Text-to-Speech - ElevenLabs with your cloned voice
    tts=elevenlabs.TTS(
        voice_id="6X0hgJwbuR7bBAFf3Krh",  # Your cloned voice ID
    ),

    # Voice Activity Detection
    vad=silero.VAD.load(),
)
```

### Adjustable Parameters

**Temperature (0.0 - 1.0):**
- Lower = More focused and deterministic
- Higher = More creative and varied
- Current: `0.8` (natural conversation)

**STT Model Options:**
- `nova-2` (recommended) - Highest accuracy
- `nova` - Fast, good accuracy
- `base` - Faster, lower accuracy

**LLM Model Options:**
- `gpt-4o-mini` (recommended) - Fast, cost-effective
- `gpt-4o` - More capable, slower
- `gpt-4-turbo` - Most capable

---

## 🎯 Synctrack Services

Sylvia can explain these services in detail:

### 1. AI Lead Generation
- Automated lead capture and qualification
- Multi-channel lead generation (web, voice, chat)
- Smart lead scoring and routing
- Integration with existing CRM systems

### 2. Workflow Automation
- Custom business process automation
- Integration with existing tools (CRMs, email, databases)
- Data synchronization and reporting
- Workflow optimization consulting

### 3. Voice AI Agents
- 24/7 conversational AI assistants
- Lead qualification via voice
- Customer support automation
- Appointment scheduling and routing

### 4. Modern Website Development
- High-converting business websites
- AI-powered features and chatbots
- Mobile-responsive design
- SEO optimization

### 5. CRM & Reporting Automation
- Automated CRM updates and management
- Real-time dashboards and analytics
- Custom reporting systems
- Data pipeline development

**Value Proposition:**
> "Automation that drives business growth. We combine AI and data workflows to make SMBs faster, smarter, and more profitable."

---

## 🐛 Troubleshooting

### Common Issues

#### 1. ElevenLabs API Key Error
```
ValueError: ElevenLabs API key is required
```

**Solution:**
- Verify `.env` has `ELEVEN_API_KEY` set
- Check API key has full permissions in ElevenLabs dashboard
- Regenerate API key if needed

#### 2. Voice Not Playing
```
WARNING: websocket closed unexpectedly
```

**Solutions:**
- Check ElevenLabs voice ID is correct
- Verify API key permissions
- Test API key with curl:
```bash
curl -X GET "https://api.elevenlabs.io/v1/voices" \
  -H "xi-api-key: YOUR_API_KEY"
```

#### 3. Model Download Timeout
```
RuntimeError: Could not find model livekit/turn-detector
```

**Solution:**
- First run may take time downloading models
- Ensure stable internet connection
- Models are cached after first download

#### 4. Python Version Error
```
ERROR: Python 3.9+ required
```

**Solution:**
```bash
python --version  # Check version
# Install Python 3.9+ if needed
```

#### 5. Import Errors
```
ModuleNotFoundError: No module named 'livekit'
```

**Solution:**
```bash
cd "Synctrack voice agent"
uv sync  # Reinstall dependencies
```

### Debug Mode

Enable verbose logging:

```bash
# In .env file
LOG_LEVEL=DEBUG
DEBUG_MODE=true
```

Then run:
```bash
uv run python sylvia_agent.py console --verbose
```

### Check Agent Logs (Cloud)

```bash
# Real-time logs
lk agent logs sylvia --follow

# Last 100 lines
lk agent logs sylvia --tail 100

# Errors only
lk agent logs sylvia | grep ERROR
```

---

## 📞 Telephony Integration (Optional)

Add phone number support to Sylvia:

### Using Twilio

1. **Set up Twilio account**: https://www.twilio.com
2. **Get a phone number**: https://console.twilio.com/phone-numbers
3. **Configure LiveKit SIP**: https://docs.livekit.io/agents/start/telephony/

### Using LiveKit Cloud

LiveKit Cloud offers built-in telephony:

```bash
lk agent create-sip-trunk --name synctrack-phone
```

Follow the wizard to:
- Select phone number
- Configure routing
- Set up billing

---

## 📚 Resources

### Documentation
- [LiveKit Agents Docs](https://docs.livekit.io/agents/) - Complete framework documentation
- [LiveKit Python SDK](https://docs.livekit.io/realtime/client/python/) - Python SDK reference
- [ElevenLabs API Docs](https://elevenlabs.io/docs/api-reference) - Voice cloning API
- [Deepgram API Docs](https://developers.deepgram.com/) - Speech recognition API
- [OpenAI API Docs](https://platform.openai.com/docs) - GPT models reference


### Community & Support
- [LiveKit Discord](https://livekit.io/discord) - Community support
- [LiveKit GitHub Issues](https://github.com/livekit/agents/issues) - Bug reports
- [LiveKit Cloud Status](https://status.livekit.io/) - Service status

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Add to `.gitignore`
2. **Rotate API keys regularly** - Especially after development
3. **Use environment variables** - Never hardcode secrets
4. **Restrict API key permissions** - Only grant necessary permissions
5. **Monitor webhook logs** - Watch for unauthorized access
6. **Use HTTPS only** - For all API endpoints
7. **Validate webhook signatures** - If supported by your CRM

---

## 📈 Performance Metrics

Based on testing in LiveKit Playground:

| Metric | Performance |
|--------|-------------|
| **Latency** | ~500-800ms (first response) |
| **STT Accuracy** | 98%+ (Deepgram Nova-2) |
| **Voice Quality** | Natural, cloned (ElevenLabs) |
| **Uptime** | 99.9% (LiveKit Cloud) |
| **Concurrent Users** | Scales automatically |

---

## 🎨 Customization

### Change Sylvia's Personality

Edit `sylvia_agent.py:42-82` to modify:
- Greeting style
- Conversation approach
- Service descriptions
- Lead qualification strategy

### Add New Function Tools

```python
@function_tool
async def your_custom_tool(self, context: RunContext, param: str) -> str:
    """Your tool description."""
    # Your logic here
    return "Response for Sylvia to speak"
```

### Modify CRM Webhook

Update `sylvia_agent.py:29` and `sylvia_agent.py:117-145`

---

## 📝 Project Structure

```
Synctrack voice agent/
├── sylvia_agent.py          # Main agent code
├── pyproject.toml           # Dependencies
├── .env                     # Environment variables (gitignored)
├── .env.example             # Environment template
├── README.md                # This file
├── .gitignore              # Git ignore rules
└── .venv/                  # Virtual environment (auto-created)
```

---

## 📄 License

This project is proprietary to Synctrack. All rights reserved.

---

## 🎉 Success!

Congratulations! You've successfully deployed Sylvia, your AI voice agent.

**Next Steps:**
1. Test in LiveKit Playground: https://agents-playground.livekit.io/
2. Monitor webhook for lead captures
3. Integrate with your website
4. Add phone number support (optional)
5. Customize personality and services

---

Using [LiveKit](https://livekit.io) • [ElevenLabs](https://elevenlabs.io) • [OpenAI](https://openai.com) • [Deepgram](https://deepgram.com)

**Questions?** Contact: hello@synctrack.com
