import socket
import threading
import numpy as np
import base64
import os
import itertools

# --- McEliece Crypto Logic (from original script) ---

def rand_full_rank_matrix(k, n, seed=None):
    """Generates a random k x n matrix over GF(2) with full rank k."""
    rnd = np.random.RandomState(seed)
    while True:
        M = rnd.randint(0, 2, size=(k, n), dtype=np.uint8)
        if gf2_rank(M) == k:
            return M

def gf2_rank(A):
    """Computes the rank of a matrix over GF(2)."""
    A = A.copy() % 2
    k, n = A.shape
    r = 0
    row = 0
    for col in range(n):
        pivot = None
        for i in range(row, k):
            if A[i, col]:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != row:
            A[[pivot, row]] = A[[row, pivot]]
        for i in range(k):
            if i != row and A[i, col]:
                A[i] ^= A[row]
        row += 1
        r += 1
        if row == k:
            break
    return r

def pack_flag_bits(flag_str, k):
    """Converts a flag string to a bit vector of length k."""
    bits = []
    for ch in flag_str.encode('utf-8'):
        for i in range(8):
            bits.append((ch >> (7 - i)) & 1)
    if len(bits) > k:
        raise ValueError("k is too small for the given flag")
    bits += [0] * (k - len(bits))
    return np.array(bits[:k], dtype=np.uint8)

def random_error(n, weight, seed=None):
    """Generates a random error vector of length n and weight t."""
    rnd = np.random.RandomState(seed)
    idx = rnd.choice(n, size=weight, replace=False)
    e = np.zeros(n, dtype=np.uint8)
    e[idx] = 1
    return e

# --- Server Logic ---

def send_line(s, msg_bytes):
    """Sends a bytes message to the client with a newline."""
    s.sendall(msg_bytes + b'\n')

def handle_client(conn, addr):
    """Handles a single client connection."""
    print(f"[+] Connection from {addr}")
    conn.settimeout(60) # 60 seconds timeout

    try:
        # ====== Problem Generation ======
        seed = 20251013
        
        # --- Flag and Parameters ---
        flag = "E4syCTF{Th1s_1s_n0t_McEl1ec3_but_a_Syndr0me_Dec0d1ng_Pr0bl3m}"
        flag_bits_len = len(flag.encode('utf-8')) * 8
        k = flag_bits_len
        redundancy = 16  # Medium-Hard: n = k + 16
        n = k + redundancy
        t = 2            # Weight of error vector (Medium-Hard: nC2 combinations)

        # 1) Generate full-rank generator matrix G (k x n)
        G = rand_full_rank_matrix(k, n, seed=seed)

        # 2) Encode flag into message vector m (k bits)
        m = pack_flag_bits(flag, k)

        # 3) Compute codeword c0
        c0 = (m.dot(G) % 2).astype(np.uint8)

        # 4) Choose error vector e
        e = random_error(n, t, seed=seed + 1)

        # 5) Compute ciphertext c
        c = (c0 ^ e).astype(np.uint8)
        
        # ====== Send Problem to Client ======
        send_line(conn, b"Welcome to the Mini-McEliece Challenge!")
        send_line(conn, b"I will give you a public key G and a ciphertext c.")
        send_line(conn, b"Your task is to find the original message m, which is the flag.")
        send_line(conn, b"All data is Base64 encoded.")
        send_line(conn, b"")
        send_line(conn, f"Parameters: n={n}, k={k}, t={t}".encode('utf-8'))
        send_line(conn, b"")
        send_line(conn, b"Note: This is a syndrome decoding problem.")
        send_line(conn, b"The error vector has a small weight, making brute-force feasible.")
        
        # Send G
        g_b64 = base64.b64encode(G.tobytes())
        send_line(conn, b"G (shape: " + f"({k},{n}))".encode('utf-8') + b": " + g_b64)

        # Send c
        c_b64 = base64.b64encode(c.tobytes())
        send_line(conn, b"c: " + c_b64)
        
        # ====== Receive and Check Answer ======
        send_line(conn, b"\nEnter your answer (the flag):")
        
        client_answer = conn.recv(1024).strip()
        
        if client_answer.decode('utf-8') == flag:
            send_line(conn, b"Correct! Congratulations!")
            print(f"[*] Correct flag received from {addr}")
        else:
            send_line(conn, b"Wrong answer.")
            print(f"[*] Wrong answer received from {addr}")

    except socket.timeout:
        print(f"[-] Connection from {addr} timed out.")
    except Exception as e:
        print(f"[!] An error occurred with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Connection from {addr} closed.")


def main():
    """Main function to start the TCP server."""
    host = '0.0.0.0'
    port = 13337

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()