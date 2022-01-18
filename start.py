from duty import app

if __name__ == "__main__":
    import sys
    port = 5000
    host = "localhost"
    for i, arg in enumerate(sys.argv):
        if arg == '--port':
            port = sys.argv[i+1]
            try:
                port = int(port)
            except ValueError:
                raise Exception('Аргумент --port должен быть цифрой в диапазоне от 1 до 65536')  # noqa
        elif arg == '--host':
            host = sys.argv[i+1]

    app.run(host=host, port=port)
