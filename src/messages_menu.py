from menu import Menu
from messages_utils import get_conversations, get_messages, send_message
from user_utils import get_user, is_plus, get_friends, get_all_users
import datetime


class MessagesMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
        self.user = get_user()
        self.title = "Messages"
        self.setup_options()

    def setup_options(self):
        conversations = get_conversations(self.user)

        for recipient in conversations:
            def run_conversation(): return self.open_conversation(
                recipient)

            self.options[f"{recipient}"] = run_conversation

        self.options["Start new conversation"] = self.on_new_conversation

    def on_new_conversation(self):
        options = self.get_recipient_options()

        print("You can send a message to:\n")
        for option in options:
            print(option)

        while True:
            receiver = input("Who are you sending the message to? ")

            if receiver in options:
                break

            print("This is not a valid user choice.")

        self.open_conversation(receiver)

    def get_recipient_options(self):
        options = get_all_users() if is_plus(self.user) else get_friends(self.user)
        return options

    def open_conversation(self, receiver):
        ConversationMenu(self.user, receiver).run()


class ConversationMenu(Menu):
    def __init__(self, sender, receiver) -> None:
        super().__init__()
        self.sender = sender
        self.receiver = receiver
        self.title = f"Conversation with {receiver}"
        self.options["Write Message"] = self.new_message

    def new_message(self):
        content = input("Input your message: ")
        send_message(self.sender, self.receiver, content)

    def pre_options(self):
        messages = get_messages(self.sender, self.receiver)
        message_lines = ""

        for sender, _, content, epoch_time in messages:
            timestamp = datetime.datetime.fromtimestamp(epoch_time)
            format = f"%D %r"

            entry = f"From {sender} at {timestamp.strftime(format)}: {content}\n"
            message_lines += entry

        return message_lines + "\n"
