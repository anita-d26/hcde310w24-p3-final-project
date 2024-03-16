from flask import Flask, render_template, request, url_for, redirect
import requests
import keys

app = Flask(__name__, static_folder='static')

# example query
query = "Hozier"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    # query = request.args.get('q')
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
    authorization_code = request.args.get('code')
    access_token = exchange_code_for_token(authorization_code)
    if access_token:
        # Store access_token securely (e.g., in a session)
        return redirect(url_for('index'))
    else:
        return "Failed to obtain access token"

def exchange_code_for_token(authorization_code):
    token_url = "https://api.genius.com/oauth/token"
    data = {
        "code": authorization_code,
        "client_id": keys.GENIUS_CLIENT_ID,
        "client_secret": keys.GENIUS_CLIENT_SECRET,
        "redirect_uri": keys.GENIUS_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    headers = {
        'User-Agent': 'CompuServe Classic/1.22',
        'Accept': 'application/json'
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        return access_token
    else:
        print("Error:", response.status_code)
        return None



if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))