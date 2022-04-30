import os
import json

import requests
from dotenv import load_dotenv

load_dotenv('../.env')

book_id = os.getenv('GOOGLE_BOOK_ID', None)
url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
params = {'key': os.getenv('GOOGLE_BOOKS_KEY', None)}
response = requests.get(url=url, params=params)

with open('books_response', 'w') as f:
    json.dump(response.json(), f, indent=4)
