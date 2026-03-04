from flask import Flask, request, Response
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # This lets your HTML talk to it

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return {'error': 'No URL'}, 400
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/youtube-search')
def youtube_search():
    query = request.args.get('q')
    if not query:
        return {'error': 'No query'}, 400
    
    # Use public API to avoid YouTube blocking
    api_url = f"https://pipedapi.kavin.rocks/search?q={query}"
    try:
        resp = requests.get(api_url)
        return Response(resp.content, mimetype='application/json')
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)