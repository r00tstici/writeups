.PHONY := build
port = 8888
app = bin/server
flag = -lsqlite3 -s

build:
	gcc main.c lib/*.c $(flag) -o $(app)

run: build
	./$(app) $(port)
