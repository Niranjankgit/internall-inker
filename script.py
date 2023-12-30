from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_urls_from_sitemap(sitemap_url):
    try:
        response = requests.get(sitemap_url)
        soup = BeautifulSoup(response.content, 'xml')
        urls = [loc.text for loc in soup.find_all('loc')]
        return urls
    except Exception as e:
        return [f"Error processing {sitemap_url}: {str(e)}"]

@app.route('/', methods=['GET', 'POST'])
def index():
    results = ""
    if request.method == 'POST':
        sitemap_urls = request.form['sitemap_urls'].split('\n')
        for sitemap_url in sitemap_urls:
            urls = extract_urls_from_sitemap(sitemap_url)
            results += f"Sitemap: {sitemap_url}\n" + "\n".join(urls) + "\n\n"
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
