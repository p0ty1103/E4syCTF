#!/usr/bin/env python3
import socket
import subprocess
import os

HOST = '0.0.0.0'
PORT = 14000

def handle_client(conn):
    proc = subprocess.Popen(
        ["./gomoku"],
        stdin=conn.makefile("rb"),
        stdout=conn.makefile("wb"),
        stderr=subprocess.STDOUT
    )
    proc.wait()
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Listening on {HOST}:{PORT} ...")

        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()