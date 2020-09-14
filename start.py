from idm import app

if __name__ == "__main__":
    import sys
    port = None
    for i, arg in enumerate(sys.argv):
        if arg == '--port':
            port = sys.argv[i+1]
            try:
                port = int(port)
                break
            except ValueError:
                raise Exception('Аргумент --port должен быть цифрой в диапазоне от 1 до 65536')  # noqa

    app.run(host="localhost", port=port or 5000)
