import random
from typing import List
import numpy as np

# fpylllが利用できない場合の代替実装
try:
    from fpylll import LLL, BKZ, IntegerMatrix
    FPYLLL_AVAILABLE = True
except ImportError:
    FPYLLL_AVAILABLE = False
    print("警告: fpylllがインストールされていません。簡易版のLLL実装を使用します。")

def gen_superincreasing_sequence(n: int, start: int = 2) -> List[int]:
    seq = []
    total = 0
    for _ in range(n):
        next_val = total + random.randint(1, start)
        seq.append(next_val)
        total += next_val
    return seq

def gen_knapsack_keys(n: int = 8, vulnerable: bool = True):
    if vulnerable:
        w = gen_superincreasing_sequence(n, start=1)
        q = sum(w) + random.randint(1, 10)
    else:
        w = gen_superincreasing_sequence(n)
        q = random.randint(sum(w) + 1, sum(w) * 2)
    
    while True:
        r = random.randint(2, q - 1)
        if gcd(r, q) == 1:
            break
    b = [(r * wi) % q for wi in w]
    return {'private': (w, q, r), 'public': b}

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def knapsack_encrypt(plaintext: str, public_key: List[int]) -> List[int]:
    ciphertext = []
    for c in plaintext.encode():
        bits = [(c >> i) & 1 for i in reversed(range(8))]
        s = sum(bit * pk for bit, pk in zip(bits, public_key))
        ciphertext.append(s)
    return ciphertext


if __name__ == "__main__":
    flag = "E4syCTF{JUCK's_delicious_sweets_were_hidden_in_knapsack}"
    keys = gen_knapsack_keys(vulnerable=True)
    public_key = keys['public']
    private_key = keys['private']
    with open("output.txt","w",encoding="utf16") as o:
        print("ฅ^-ﻌ-^ฅ < Happy Halloween! I gave you my sweets:",file=o)
        print(f"public_key:{public_key}",file=o)
        encrypted = knapsack_encrypt(flag, public_key)
        print(f"encrypted_flag:{encrypted}",file=o)
