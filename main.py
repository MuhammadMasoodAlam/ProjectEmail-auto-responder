# main.py

import time
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
    def fetch_new_emails(self):
        print("Kickoff the Email Filter Crew")
        new_emails = [
            Email(sender="example1@example.com", subject="Hello", body="How are you?"),
            Email(sender="example2@example.com", subject="Meeting", body="Let's schedule a meeting.")
        ]
        updated_checked_email_ids = {email.subject for email in new_emails}

        self.state.emails = new_emails
        self.state.checked_emails_ids = updated_checked_email_ids

    @listen(fetch_new_emails)
    def generate_draft_responses(self):
        print("Current email queue: ", len(self.state.emails))
        if len(self.state.emails) > 0:
            print("Writing New emails")
            emails = [email.dict() for email in self.state.emails]

            EmailFilterCrew().crew().kickoff(inputs={"emails": emails})

            self.state.emails = []

        print("Waiting for 180 seconds")
        time.sleep(180)

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

if __name__ == "__main__":
    kickoff()