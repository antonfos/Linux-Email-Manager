#!/usr/bin/python

from appsrc import app

if __name__ == "__main__":
    app.debug = True
    app.run("127.0.0.1", 5000)