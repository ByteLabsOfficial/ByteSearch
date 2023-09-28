from flask import Flask, request, render_template, jsonify, redirect, make_response
from flask_cors import CORS
from duckduckgo_search import DDGS
from pytrends.request import TrendReq
import json

app = Flask(__name__)
app.static_folder = "static"
CORS(app, resources={r"/*": {"origins": "*"}})
pytrends = TrendReq(hl='en-US', tz=360)

rootPath = "./"
rootPath = "/home/ByteSearch/mysite/"


@app.route("/")
def main_search_page():
    return render_template("index.html")


@app.route("/search")
def get_search_results():
    userid = request.cookies.get("user_id")
    searchPrompt = request.args.get('q')

    if userid == None:
        return redirect("https://bluelink.pythonanywhere.com/get_user_id")

    searchResults = []
    answerLst = []
    with DDGS() as ddgs:
        for r in ddgs.text(searchPrompt, region='wt-wt', safesearch='on', timelimit='y', backend="lite"):
            searchResults.append(r)
        for r in ddgs.answers(searchPrompt):
            answerLst.append(r)

    with open(f"{rootPath}search.json", "r") as file:
        data = json.load(file)
    if userid not in data:
        data[userid] = []
    data[userid].append(searchPrompt)

    with open(f"{rootPath}search.json", "w") as file:
        json.dump(data, file, indent=2, separators=(",", ": "))

    return render_template("searchPage.html", searchPrompt=searchPrompt, searchResults=searchResults, answerLst=answerLst, userid=userid)


@app.route("/search_api", methods=["POST"])
def get_search_results_api():
    searchPrompt = request.args.get('q')

    searchResults = []
    with DDGS() as ddgs:
        for r in ddgs.text(searchPrompt, region='wt-wt', safesearch='on', timelimit='y', backend="lite"):
            searchResults.append(r)
    print(searchResults)
    return jsonify(searchResults)


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
    return render_template("imageSearch.html", searchPrompt=searchPrompt, searchResults=searchResults[0:100])


@app.route('/trending', methods=["POST"])
def get_trending_data():
    trendsData = pytrends.trending_searches(pn='united_states')
    trendsLst = trendsData.values.tolist()
    return jsonify(trendsLst)


@app.route("/getsearchhistory", methods=["POST"])
def get_searchhistory():
    with open(f"{rootPath}search.json", "r") as file:
        data = json.load(file)

    userid = request.args.get('userid')
    if not userid in data:
        return "User not found", 404

    return jsonify(data[userid])


@app.route("/userid")
def set_userid():
    userid = request.args.get('id')
    resp = make_response(redirect(f"/", code=302))
    resp.set_cookie("user_id", str(userid), path="/")
    return resp
