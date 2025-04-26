import requests
import environ
import logging
import sys

env = environ.Env()
environ.Env.read_env('.env')

class TrelloAPI:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(levelname)s - %(asctime)s] %(message)s',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger()
        self.api_key = env("TRELLO_API_KEY")
        self.token = env("TRELLO_TOKEN")
        self.list_id = env("TRELLO_LIST_ID")

    def create_card(self, client_name: str, ticket_level: str, ticket_description: str) -> bool:
        url = "https://api.trello.com/1/cards"
        query = {
            'key': self.api_key,
            'token': self.token,
            'idList': self.list_id,
            'name': f"[{ticket_level}] - [{client_name}]",
            'desc': ticket_description,
        }
        response = requests.post(url, params=query)
        if response.status_code == 200:
            self.logger.info(f"Card {client_name}, {ticket_level}, {ticket_description} created successfully")
            return True
        else:
            self.logger.error(f"Error creating card: {response.status_code}, {response.text}")
            return False

if __name__ == "__main__":
    trello = TrelloAPI()
    
    trello.create_card("Asanali", "HIGH", "Help me my headlight is broken")