from flask import Flask, request, render_template
from duckduckgo_search import DDGS

app = Flask(__name__)
app.static_folder = "static"


@app.route("/search")
def get_search_results():
    searchPrompt = request.args.get('q')

    searchResults = []
    with DDGS() as ddgs:
        for r in ddgs.text(searchPrompt, region='wt-wt', safesearch='Off', timelimit='y'):
            searchResults.append(r)
    return render_template("index.html", searchPrompt=searchPrompt, searchResults=searchResults)
