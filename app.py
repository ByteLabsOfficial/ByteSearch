from flask import Flask, request, render_template
from duckduckgo_search import DDGS

app = Flask(__name__)
app.static_folder = "static"


@app.route("/")
def main_search_page():
    return render_template("index.html")


@app.route("/search")
def get_search_results():
    searchPrompt = request.args.get('q')

    searchResults = []
    with DDGS() as ddgs:
        for r in ddgs.text(searchPrompt, region='wt-wt', safesearch='Off', timelimit='y'):
            searchResults.append(r)
    return render_template("searchPage.html", searchPrompt=searchPrompt, searchResults=searchResults)


@app.route("/image")
def get_image_results():
    searchPrompt = request.args.get('q')

    searchResults = []
    with DDGS() as ddgs:
        keywords = searchPrompt
        ddgs_images_gen = ddgs.images(
            keywords,
            region="wt-wt",
            safesearch="Off",
            size=None,
            type_image=None,
            layout=None,
            license_image=None,
        )
        for r in ddgs_images_gen:
            searchResults.append(r)
    return render_template("imageSearch.html", searchPrompt=searchPrompt, searchResults=searchResults)
