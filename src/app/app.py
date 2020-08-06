from flak import Flask

app = Flask()


if __name__ == '__main__':
    app.run(debug=True, host=127.0.0.1, port=80)
