from google_auth_oauthlib.flow import InstalledAppFlow
import requests
from database.db import Database

def google_login():
    # OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_sceret.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
    )
    creds = flow.run_local_server(port=0)

    # Use token to get user info
    response = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {creds.token}'}
    )
    profile_info = response.json()

    username = profile_info['username']
    email = profile_info['email']

    # Save to DB using your Database class
    db = Database()
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        connection.commit()

    cursor.close()
    connection.close()

    return {"username": username, "email": email}
