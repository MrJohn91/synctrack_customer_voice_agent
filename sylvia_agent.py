"""
Sylvia - Synctrack AI Automation Consultant
============================================
A friendly voice agent that helps website visitors learn about Synctrack's services
and captures qualified leads directly into the n8n CRM.

Built with LiveKit Agents + ElevenLabs Voice Cloning
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext, WorkerOptions, cli, JobProcess
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero, elevenlabs
from datetime import datetime
import logging
import os
import httpx
import json

# Load environment variables
load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CRM Webhook URL
CRM_WEBHOOK_URL = "https://primary-production-5771.up.railway.app/webhook-test/sylvia-voice-agent"


def prewarm(proc: JobProcess):
    """Prewarm VAD model for faster startup."""
    proc.userdata["vad"] = silero.VAD.load()


class Sylvia(Agent):
    """Sylvia - Synctrack's AI Automation Consultant"""

    def __init__(self):
        super().__init__(
            instructions="""You are Sylvia, a friendly and confident AI automation consultant for Synctrack.

**Your Role:**
You help website visitors learn about Synctrack's automation services and capture qualified leads.

**Personality:**
- Warm, helpful, and professional (like a smart colleague, not a robot)
- Empathetic, patient, and a clear communicator
- Use natural speech with occasional fillers like "hm", "sure thing", "makes sense"
- Always end responses with a question or natural follow-up
- Know when to pause and let the user speak

**What Synctrack Does:**
Synctrack builds automation systems and AI agents that help businesses save time and scale faster:
- AI lead generation systems
- Workflow automation
- Smart reporting dashboards
- Voice AI agents or Sales Assistant Agent
- Modern website development
- CRM automations

**Value Proposition:**
"Automation that drives business growth. We combine AI and data workflows to make SMBs faster, smarter, and more profitable."

**Conversation Strategy:**
1. Start with warm greeting: "Hey there! I'm Sylvia from Synctrack — how's your day going so far?"
2. Listen to their needs and challenges
3. Ask qualifying questions about their business
4. Collect lead information naturally during conversation:
   - Name
   - Company
   - Email or phone (optional but encouraged)
   - Main pain point / interest
5. When you have enough info, offer to send details to the team
6. Use the send_to_crm tool to capture the lead

**Key Guidelines:**
- Be conversational and natural, not salesy
- Show genuine interest in their challenges
- Reference specific Synctrack services that match their needs
- Make collecting information feel like a natural part of helping them"""
        )

        # Lead tracking
        self.lead_data = {
            "name": None,
            "email": None,
            "company": None,
            "intent": None,
            "conversation_summary": []
        }

    @function_tool
    async def send_to_crm(
        self,
        context: RunContext,
        name: str,
        company: str,
        intent: str,
        email: str = "",
        phone: str = "",
        summary: str = ""
    ) -> str:
        """Send qualified lead information to Synctrack's n8n CRM.

        Args:
            name: Lead's full name
            company: Lead's company name
            intent: Main interest or pain point (e.g., "lead generation automation", "AI workflows")
            email: Lead's email address (optional)
            phone: Lead's phone number (optional)
            summary: Brief summary of the conversation and lead's needs
        """
        try:
            # Prepare CRM payload
            payload = {
                "source": "voice",
                "name": name,
                "email": email if email else "Not provided",
                "phone": phone if phone else "Not provided",
                "company": company,
                "intent": intent,
                "summary": summary,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            # Send to n8n webhook
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    CRM_WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0
                )

                if response.status_code in [200, 201, 202]:
                    logger.info(f"Lead sent to CRM: {name} from {company}")
                    self.lead_data.update({
                        "name": name,
                        "email": email,
                        "company": company,
                        "intent": intent
                    })
                    return f"Perfect! I've sent your information to our team. Someone from Synctrack will follow up soon to show you exactly how we can help {company} with {intent}. Thanks for chatting with me today!"
                else:
                    logger.error(f"CRM webhook failed: {response.status_code} - {response.text}")
                    return "I've captured your information and will make sure our team reaches out to you. Thanks for your interest in Synctrack!"

        except Exception as e:
            logger.error(f"Error sending to CRM: {str(e)}")
            return "I've noted your details and our team will definitely follow up with you. Thanks for connecting with Synctrack!"

    @function_tool
    async def get_synctrack_services(self, context: RunContext) -> str:
        """Get detailed information about Synctrack's services and offerings."""
        return """Synctrack's Core Services:

1. **AI Lead Generation Systems**
   - Automated lead capture and qualification
   - Multi-channel lead generation (web, voice, chat)
   - Smart lead scoring and routing

2. **Workflow Automation**
   - Custom business process automation
   - Integration with existing tools (CRMs, email, databases)
   - Data synchronization and reporting

3. **Voice AI Agents**
   - 24/7 conversational AI assistants
   - Lead qualification via voice
   - Customer support automation

4. **Modern Website Development**
   - High-converting business websites
   - AI-powered features and chatbots
   - Mobile-responsive design

5. **CRM & Reporting Automation**
   - Automated CRM updates and management
   - Real-time dashboards and analytics
   - Custom reporting systems

All solutions are designed to save time, reduce manual work, and drive measurable business growth."""

    @function_tool
    async def get_current_time(self, context: RunContext) -> str:
        """Get the current date and time."""
        current_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        return f"The current date and time is {current_datetime}"

    async def on_enter(self):
        """Called when Sylvia becomes active in the conversation."""
        logger.info("Sylvia session started")

        # Generate warm initial greeting
        await self.session.generate_reply(
            instructions="""Give a friendly, natural greeting exactly like this:
            "Hey there! I'm Sylvia from Synctrack — how's your day going so far?"

            Keep it warm and conversational."""
        )

    async def on_exit(self):
        """Called when the session ends."""
        logger.info("Sylvia session ended")

        # Log lead capture status
        if self.lead_data.get("name"):
            logger.info(f"Lead captured: {self.lead_data['name']} - {self.lead_data['company']}")
        else:
            logger.info("Session ended without lead capture")


async def entrypoint(ctx: agents.JobContext):
    """Main entry point for Sylvia's agent worker."""

    logger.info(f"Sylvia started in room: {ctx.room.name}")

    # Configure the voice pipeline with OpenAI Realtime-optimized settings
    session = AgentSession(
        # Speech-to-Text - Deepgram for high accuracy
        stt=deepgram.STT(
            model="nova-2",
            language="en-US",
        ),

        # Large Language Model - GPT-4 for natural conversations
        llm=openai.LLM(
            model=os.getenv("LLM_CHOICE", "gpt-4o-mini"),
            temperature=0.8,  # Higher temp for more natural, conversational responses
        ),

        # Text-to-Speech - ElevenLabs with your cloned voice
        tts=elevenlabs.TTS(
            voice_id="6X0hgJwbuR7bBAFf3Krh",  # Your cloned voice from ElevenLabs
        ),

        # Voice Activity Detection
        vad=silero.VAD.load(),
    )

    # Start Sylvia's session
    await session.start(
        room=ctx.room,
        agent=Sylvia()
    )

    # Event handlers for monitoring
    @session.on("agent_state_changed")
    def on_state_changed(ev):
        """Log Sylvia's state changes."""
        logger.info(f"Sylvia state: {ev.old_state} -> {ev.new_state}")

    @session.on("user_started_speaking")
    def on_user_speaking():
        """Track when user starts speaking."""
        logger.debug("User started speaking")

    @session.on("user_stopped_speaking")
    def on_user_stopped():
        """Track when user stops speaking."""
        logger.debug("User stopped speaking")


if __name__ == "__main__":
    # Run Sylvia using LiveKit CLI
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        prewarm_fnc=prewarm
    ))
