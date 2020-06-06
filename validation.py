# -*- coding: UTF-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route("/.well-known/pki-validation/<filename>")
def sslForFree(filename):
    with open("sslforfree.txt", "r") as fin:
        return fin.read()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)

