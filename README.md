# Extract Data from Article on Web
Application from scraping data from a website (news/article)

## Contents

Application gets the data from the website.
Parses through dates/days & tags them.
Parses through abbreviations & expands them under a tag.

## Setup

cd into the ../ folder:

Install dependencies:

```sh
pip install -r requirements.txt
```

To launch a dev server:

```sh
uvicorn main:app --reload
```

Browser (for better experience - Swagger UI):

```sh
http://localhost:8000/docs
```