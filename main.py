import asyncio
from typing import List
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from email_auto_responder_flow.types import Email
from email_auto_responder_flow.email_filter_crew.email_filter_crew import EmailFilterCrew

class AutoResponderState(BaseModel):
    emails: List[Email] = []
    checked_emails_ids: set[str] = set()

class EmailAutoResponderFlow(Flow[AutoResponderState]):
    initial_state = AutoResponderState

    @start("wait_next_run")
    def fetch_new_emails(self) -> List[Email]:
        # Fetch new emails from the server (dummy data for illustration)
        emails = [
            Email(
                id="1",
                threadId="thread1",
                snippet="Hello, how are you?",
                sender="example1@example.com",
                subject="Hello",
                body="How are you?"
            ),
            Email(
                id="2",
                threadId="thread2",
                snippet="Meeting tomorrow",
                sender="example2@example.com",
                subject="Meeting Reminder",
                body="Don't forget our meeting tomorrow at 10 AM."
            )
        ]
        self.state.emails.extend(emails)
        return emails

    @listen(fetch_new_emails)
    async def generate_draft_responses(self):
        print("Current email queue: ", len(self.state.emails))
        if len(self.state.emails) > 0:
            print("Writing New emails")
            emails = [email.dict() for email in self.state.emails]

            await EmailFilterCrew().crew().kickoff(inputs={"emails": emails})

            self.state.emails = []

        print("Waiting for 180 seconds")
        await asyncio.sleep(180)

def kickoff():
    """
    Run the flow.
    """
    email_auto_response_flow = EmailAutoResponderFlow()
    email_auto_response_flow.kickoff()

def plot_flow():
    """
    Plot the flow.
    """
    email_auto_response_flow = EmailAutoResponderFlow()
    email_auto_response_flow.plot()

# Assuming the rest of your main.py file looks something like this
if __name__ == "__main__":
    kickoff()