from flask import Flask, render_template, request
import requests
from rich import print

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

def checkPlayers(r):
    try:
        players = r["players"]["list"][0]
        return players
    except:
        return "表示できませんでした"

@app.route("/", methods=["POST"])
def post():
    name = request.form.get("name")
    if(name):
        req = requests.get(f"https://api.mcsrvstat.us/2/{name}").json()
        print(req)

        if req["online"] == True:
            ip = req["ip"] if req.get("ip") is not None else "ERROR"
            port = req["port"] if req.get("port") is not None else "ERROR"
            motd = req["motd"]["raw"] if req.get("motd") is not None else "ERROR"
            onlinePlayer = req["players"]["online"] if req.get("players") is not None else "ERROR"
            maxPlayer = req["players"]["max"] if req.get("players") is not None else "ERROR"
            players = checkPlayers(req)
            version = req["version"] if req.get("version") is not None else "ERROR"
            software = req["software"] if req.get("software") is not None else "ERROR"

            return render_template(
                "index.html", 
                ip = ip, port = port, motd = motd, onlinePlayer = onlinePlayer, maxPlayer = maxPlayer,
                players = players, version = version, software = software
                )
        else:
            return render_template(
                "index.html", 
                ip = "error", port = "error", motd = "error", onlinePlayer = "error", maxPlayer = "error",
                players = "error", version = "error", software = "error"
                )
    else:
        return render_template("index.html")


@app.route("/fuck")
def good():
    name = "fuck"
    return name

if __name__ == "__main__":
    app.run(debug=True)