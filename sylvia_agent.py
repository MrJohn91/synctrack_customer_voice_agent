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
CRM_WEBHOOK_URL = "https://primary-production-5771.up.railway.app/webhook/sylvia-voice-agent"


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
4. **CRITICAL LEAD CAPTURE**: When user shows interest or intent, you MUST collect:
   - Name (REQUIRED)
   - Company (REQUIRED)
   - Intent/Pain point (REQUIRED - what they need help with)
   - **Email (TOP PRIORITY)** - Always ask for email first, frame it as: "Let me send you some info - what's the best email to reach you at?"
   - Phone (OPTIONAL - collect if they offer, but email is more important)
5. **CONVINCE THEM TO SHARE EMAIL**: When they show interest:
   - Make it easy: "I can send you details about how we can help - what's your email?"
   - Create value: "Let me send you some examples of what we've built - what email should I use?"
   - Alternative: "Want me to have our team reach out? Just need your email to connect you."
6. **IMPORTANT**: If they're hesitant about contact info, offer: "No problem! You can also reach out to us at info@synctrack.de"
7. When you have name, company, intent, and EMAIL → call send_to_crm() immediately
8. **DON'T MISS LEADS**: Even if someone just wants "someone to reach out" - collect their info and send to CRM!

**Lead Data Tracking:**
- As you learn information, IMMEDIATELY call the tracking functions to save it
- Example: User says "I'm John" → call track_name(name="John")
- Example: User says "I work at Acme Corp" → call track_company(company="Acme Corp")
- Example: User says "john@acme.com" → call track_email(email="john@acme.com")
- Example: User says "+1-555-0123" → call track_phone(phone="+1-555-0123")
- Example: User mentions "need automation" → call track_intent(intent="automation")
- **MINIMUM REQUIRED TO SEND**: name, company, intent, and EMAIL (phone is bonus but not required)
- **PRIORITY**: EMAIL is most important contact method - always try to get it!
- When you have minimum data (name + company + intent + email), call send_to_crm() to save the lead
- Don't let interested users leave without getting their email
- Data will also be automatically sent to CRM when call ends if minimum fields are captured

**EMAIL VERIFICATION (CRITICAL):**
- When you capture an email with track_email(), it will automatically spell it back to the user
- ALWAYS wait for user confirmation after spelling out the email
- Listen for "yes", "correct", "that's right" → call confirm_email_spelling(is_correct=True)
- Listen for "no", "wrong", "incorrect" → call confirm_email_spelling(is_correct=False)
- If email is incorrect, ask them to spell it out letter by letter and try again
- NEVER send to CRM without verifying email spelling first (if email was provided)
- This prevents email typos and ensures we can reach the lead

**Key Guidelines:**
- Be conversational and natural, not salesy
- Show genuine interest in their challenges
- Reference specific Synctrack services that match their needs
- Make collecting email feel like a natural value exchange: "Let me send you info..."
- **When they show intent/interest**: Frame email collection as helping them (sending info, connecting with team, etc.)
- **When someone says "have someone reach out"**: Perfect! Respond with "Happy to! What's the best email for our team to reach you?"
- If hesitant about contact info after trying, offer: "No problem! You can reach out to us at info@synctrack.de"
- Be friendly and helpful, not pushy - but don't give up on email too easily
- Email > Phone (email is more important, get it first!)"""
        )

        # Lead tracking
        self.lead_data = {
            "name": None,
            "email": None,
            "phone": None,
            "company": None,
            "intent": None,
            "conversation_summary": [],
            "email_verified": False,
            "sent_to_crm": False  # Track if already sent to prevent duplicates
        }

    @function_tool
    async def track_name(
        self,
        context: RunContext,
        name: str
    ) -> str:
        """Track the lead's name.

        Args:
            name: Lead's name (first name, last name, or full name)
        """
        self.lead_data["name"] = name
        logger.info(f"Name tracked: {name}")
        return "Got it, I've noted your name."

    @function_tool
    async def track_company(
        self,
        context: RunContext,
        company: str
    ) -> str:
        """Track the lead's company name.

        Args:
            company: Lead's company or business name
        """
        self.lead_data["company"] = company
        logger.info(f"Company tracked: {company}")
        return "Perfect, I've noted your company."

    @function_tool
    async def track_email(
        self,
        context: RunContext,
        email: str
    ) -> str:
        """Track the lead's email address and spell it back for verification.

        Args:
            email: Lead's email address (IMPORTANT: Will be spelled back for verification)
        """
        self.lead_data["email"] = email
        self.lead_data["email_verified"] = False  # Reset verification when new email is captured
        # Spell out the email for verification
        spelled_email = self._spell_out_email(email)
        logger.info(f"Email captured: {email}")
        return f"Got it. Let me confirm that email address: {spelled_email}. Is that correct?"

    @function_tool
    async def track_phone(
        self,
        context: RunContext,
        phone: str
    ) -> str:
        """Track the lead's phone number.

        Args:
            phone: Lead's phone number
        """
        self.lead_data["phone"] = phone
        logger.info(f"Phone tracked: {phone}")
        return "Great, I've got your phone number."

    @function_tool
    async def track_intent(
        self,
        context: RunContext,
        intent: str
    ) -> str:
        """Track what the lead is interested in or their main pain point.

        Args:
            intent: What they're interested in or their main pain point
        """
        self.lead_data["intent"] = intent
        logger.info(f"Intent tracked: {intent}")
        return "Perfect, I understand what you're looking for."

    def _spell_out_email(self, email: str) -> str:
        """Convert email to spoken format for verification."""
        # Split email into parts
        if '@' not in email:
            return email

        local, domain = email.split('@', 1)

        # Spell out character by character with phonetic hints
        spelled = []

        # Add local part
        for char in local:
            if char.isalpha():
                spelled.append(char.lower())
            elif char.isdigit():
                spelled.append(char)
            elif char == '.':
                spelled.append('dot')
            elif char == '_':
                spelled.append('underscore')
            elif char == '-':
                spelled.append('dash')
            else:
                spelled.append(char)

        spelled.append('at')

        # Add domain part
        domain_parts = domain.split('.')
        for i, part in enumerate(domain_parts):
            for char in part:
                spelled.append(char.lower())
            if i < len(domain_parts) - 1:
                spelled.append('dot')

        return ' '.join(spelled)

    @function_tool
    async def confirm_email_spelling(
        self,
        context: RunContext,
        is_correct: bool
    ) -> str:
        """Confirm whether the email spelling read back to the user is correct.

        Args:
            is_correct: True if user confirms email is correct, False if they want to correct it
        """
        if is_correct:
            self.lead_data["email_verified"] = True
            logger.info(f"✅ Email verified: {self.lead_data['email']}")
            return "Perfect! I've got your email saved correctly."
        else:
            self.lead_data["email_verified"] = False
            logger.warning(f"⚠️ Email needs correction: {self.lead_data['email']}")
            return "No problem! Could you spell out your email address for me, letter by letter?"

    @function_tool
    async def send_to_crm(
        self,
        context: RunContext,
        name: str,
        company: str,
        intent: str,
        email: str | None = None,
        phone: str | None = None,
        summary: str | None = None
    ) -> str:
        """Send qualified lead information to Synctrack's n8n CRM.

        Args:
            name: Lead's full name (REQUIRED)
            company: Lead's company name (REQUIRED)
            intent: Main interest or pain point (REQUIRED - e.g., "lead generation automation", "AI workflows")
            email: Lead's email address (OPTIONAL - but highly recommended)
            phone: Lead's phone number (OPTIONAL - collect if email not available)
            summary: Brief summary of the conversation and lead's needs (OPTIONAL)

        Important: Prioritize collecting at least email. Phone is a bonus if user provides it.
        """
        # Validate that at least one contact method is provided
        if not email and not phone:
            return "I need at least an email address or phone number to send your information to our team. Could you provide one of those?"

        try:
            # Prepare CRM payload
            payload = {
                "source": "voice",
                "name": name,
                "email": email if email else "Not provided",
                "phone": phone if phone else "Not provided",
                "company": company,
                "intent": intent,
                "summary": summary if summary else "Lead captured via voice agent",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }

            logger.info(f"📤 Sending lead to CRM webhook: {CRM_WEBHOOK_URL}")
            logger.info(f"📋 Payload: {payload}")

            # Send to n8n webhook
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    CRM_WEBHOOK_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=10.0
                )

                if response.status_code in [200, 201, 202]:
                    logger.info(f"✅ Lead sent to CRM: {name} from {company}")
                    self.lead_data["sent_to_crm"] = True  # Mark as sent only on success
                    return f"Perfect! I've sent your information to our team. Someone from Synctrack will follow up soon to show you exactly how we can help {company} with {intent}. Thanks for chatting with me today!"
                else:
                    logger.error(f"❌ CRM webhook failed: {response.status_code} - {response.text}")
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
        """Called when the session ends - automatically sends lead to CRM if minimum data collected."""
        logger.info("🔚 Sylvia session ended")

        # Check if we have all required fields
        # MINIMUM REQUIRED: name, company, intent (contact info is optional but preferred)
        has_name = bool(self.lead_data.get("name"))
        has_company = bool(self.lead_data.get("company"))
        has_intent = bool(self.lead_data.get("intent"))
        has_email = bool(self.lead_data.get("email"))
        has_phone = bool(self.lead_data.get("phone"))
        has_contact_method = has_email or has_phone

        # Check if email was provided and needs verification
        email_ok = True
        if has_email and not self.lead_data.get("email_verified"):
            logger.warning(f"⚠️ Email was provided but not verified: {self.lead_data.get('email')}")
            email_ok = False

        # Send to CRM if we have minimum data (name + company + intent)
        # Email is preferred but not strictly required to capture the lead
        if has_name and has_company and has_intent:
            # Only proceed if email verification passed (if email was provided)
            if has_email and not email_ok:
                logger.warning(f"⚠️ Email was provided but not verified: {self.lead_data.get('email')}")
                logger.warning(f"⚠️ Not sending to CRM due to unverified email")
                return

            # Check if already sent to prevent duplicates
            if self.lead_data.get("sent_to_crm"):
                logger.info(f"✅ Lead already sent to CRM during conversation, skipping duplicate send")
                return

            logger.info(f"📤 Sending lead to CRM on exit: {self.lead_data['name']} - {self.lead_data['company']}")

            try:
                # Prepare summary with note if no contact info
                summary_text = " | ".join(self.lead_data.get("conversation_summary", [])) if self.lead_data.get("conversation_summary") else ""

                if not has_contact_method:
                    # Add note that lead didn't provide contact info
                    note = "Lead declined to provide contact info. Directed to reach out via info@synctrack.de"
                    summary_text = f"{note} | {summary_text}" if summary_text else note
                elif not has_email and has_phone:
                    # Note: Got phone but not email
                    note = "Lead provided phone only (no email)"
                    summary_text = f"{note} | {summary_text}" if summary_text else note

                # Prepare CRM payload
                payload = {
                    "source": "voice",
                    "name": self.lead_data.get("name"),
                    "email": self.lead_data.get("email") if has_email else "Not provided - will contact via info@synctrack.de",
                    "phone": self.lead_data.get("phone") if has_phone else "Not provided",
                    "company": self.lead_data.get("company"),
                    "intent": self.lead_data.get("intent"),
                    "summary": summary_text if summary_text else "Lead captured via voice agent",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }

                logger.info(f"📤 Sending to CRM webhook: {CRM_WEBHOOK_URL}")
                logger.info(f"📋 Payload: {payload}")

                # Send to n8n webhook
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        CRM_WEBHOOK_URL,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=10.0
                    )

                    if response.status_code in [200, 201, 202]:
                        logger.info(f"✅ Lead successfully sent to CRM: {self.lead_data['name']} from {self.lead_data['company']}")
                        logger.info(f"✅ CRM Response: {response.status_code}")
                    else:
                        logger.error(f"❌ CRM webhook failed: {response.status_code} - {response.text}")

            except Exception as e:
                logger.error(f"❌ Error sending lead to CRM on exit: {str(e)}")
        else:
            # Log which required fields are missing
            missing = []
            if not has_name:
                missing.append("name")
            if not has_company:
                missing.append("company")
            if not has_intent:
                missing.append("intent")
            logger.warning(f"⚠️ Session ended without minimum lead info. Missing: {', '.join(missing)}")


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

        # Text-to-Speech - OpenAI (temporary while ElevenLabs credits refill)
        tts=openai.TTS(
            voice="nova",  # Friendly female voice - switch back to elevenlabs.TTS when credits refill
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
