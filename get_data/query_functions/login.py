from requests import get as get
from requests import post as post
import requests
import json
import bcrypt
from config import EMAIL, PASSWORD

login_url = f'https://api.sorare.com/api/v1/users/{EMAIL}'


def session_login(s, email, password):
    r = s.get(login_url)
    response = json.loads(r.content)

    # get salt and hash with password
    salt = response['salt'].encode('utf8')
    pwrd = password.encode('utf8')
    hashed = bcrypt.hashpw(pwrd, salt).decode('utf8')

    # login
    url = 'https://api.sorare.com/graphql'
    login_query = """
    mutation SignInMutation($input: signInInput!) {
      signIn(input: $input) {
        currentUser {
          slug
          __typename
        }
        otpSessionChallenge
        errors {
          path
          message
          __typename
        }
        __typename
      }
    }
    """

    variables = {
        "input": {
            "email": email,
            "password": hashed
        }
    }

    p = s.post(url, json={'query': login_query, 'OperationName': 'SignInMutation', 'variables': variables})
    return p, s


if __name__ == "__main__":
    with requests.Session() as s:
        p, s = session_login(s, email=EMAIL, password=PASSWORD)
