import os
import pickle

from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow
from llama_index import GPTSimpleVectorIndex, download_loader


os.environ['OPENAI_API_KEY'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
memory_bank = ['google-docs-id-1', 'google-docs-id-2', 'google-docs-id-3']


def authorize_gdocs():
    google_oauth2_scopes = [
        "https://www.googleapis.com/auth/documents.readonly"
    ]
    cred = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", 'rb') as token:
            cred = pickle.load(token)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", google_oauth2_scopes)
            cred = flow.run_local_server(port=0)
        with open("token.pickle", 'wb') as token:
            pickle.dump(cred, token)


if __name__ == '__main__':

    authorize_gdocs()
    GoogleDocsReader = download_loader('GoogleDocsReader')
    loader = GoogleDocsReader()
    documents = loader.load_data(document_ids=memory_bank)
    index = GPTSimpleVectorIndex(documents)

    while True:
        prompt = input("Type prompt: ")
        response = index.query(prompt)
        print(response)

        # Get the last token usage
        last_token_usage = index.llm_predictor.last_token_usage
        print(f"last_token_usage={last_token_usage}")
