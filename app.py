from flask import Flask, render_template, request, url_for, redirect
import requests
import keys

app = Flask(__name__, static_folder='static')


# example query
query = 'Hozier'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    if query:
        search_results = search_genius(query)
        return render_template('search_results.html', search_results=search_results)
    else:
        return "No search term provided."

def search_genius(query):
    url = f"https://api.genius.com/search?q={query}"
    headers = {'Authorization': f'Bearer {keys.CLIENT_ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data['response']['hits']
    else:
        return []
    

@app.route('/authorize')
def authorize():
    # Redirect the user to Genius's authentication page
    authorization_url = f"https://api.genius.com/oauth/authorize?client_id={keys.GENIUS_CLIENT_ID}&redirect_uri={keys.GENIUS_REDIRECT_URI}&response_type=code&scope=me"
    return redirect(authorization_url)


@app.route('/auth_callback')
def auth_callback():
    # Retrieve the authorization code from the query parameters
    authorization_code = request.args.get('code')

    # Exchange the authorization code for an access token
    access_token = exchange_code_for_token(authorization_code)

    # Now you have the access token, you can make authenticated requests to the Genius API
    # Store the access token securely for future use (e.g., in a session)

    return redirect(url_for('index'))

def exchange_code_for_token(authorization_code):
    token_url = "https://api.genius.com/oauth/token"
    data = {
        "code": authorization_code,
        "client_id": keys.GENIUS_CLIENT_ID,
        "client_secret": keys.GENIUS_CLIENT_SECRET,
        "redirect_uri": keys.GENIUS_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
    


if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))