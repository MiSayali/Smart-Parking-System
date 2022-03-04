from flask import Flask, render_template, jsonify

import state
import schema

schema.InitConnection()

app = Flask(__name__,
            static_folder = "./flaskvue/dist/static",
            template_folder = "./flaskvue/dist")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/api/lot')
def lot_status():
    response = {
        'state': state.GetState()
    }
    print(response)
    return jsonify(response)

