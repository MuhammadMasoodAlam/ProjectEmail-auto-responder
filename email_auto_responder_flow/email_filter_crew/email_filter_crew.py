# email_auto_responder_flow/email_filter_crew/email_filter_crew.py
import asyncio

class EmailFilterCrew:
    def crew(self):
        print("EmailFilterCrew activated.")
        return self

    async def kickoff(self, inputs):
        print(f"Processing emails: {inputs['emails']}")
        # Simulate some async processing
        await asyncio.sleep(1)
