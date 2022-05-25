from flask import Flask, redirect, url_for, render_template, request
from markupsafe import escape
import random
import mqtt

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    broker, topic = mqtt.default_broker, mqtt.default_topic 

    p = mqtt.Publisher(id = random.randint(0, 1000))
    p.connect(broker = broker, topic = topic)

    if request.method == "POST":
        p.create_message(request.form.get("nm"))
        p.publish()

    return render_template("index.html", topic = topic) 

if __name__ == "__main__":
    app.run(debug = True)
