from Crypto.Util.number import getPrime, long_to_bytes, isPrime
from random import randint

# 楕円曲線上の点の加算
def ec_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None  # 無限遠点
    if P == Q:
        lam = (3 * x1 * x1 + a) * pow(2 * y1, -1, p) % p
    else:
        lam = (y2 - y1) * pow(x2 - x1, -1, p) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

# 楕円曲線上のスカラー倍算 (Double-and-add法)
def ec_mul(P, k, a, p):
    R = None  # 無限遠点
    Q = P
    while k > 0:
        if k & 1:
            R = ec_add(R, Q, a, p)
        Q = ec_add(Q, Q, a, p)
        k >>= 1
    return R

# 平方剰余からy座標を求める
def get_y(x, a, b, p):
    y2 = (x*x*x + a*x + b) % p
    if pow(y2, (p - 1) // 2, p) != 1:
        return None # 平方非剰余
    # p = 3 (mod 4) の場合
    return pow(y2, (p + 1) // 4, p)

# --- Curve 1 (脆弱な特異曲線 y^2 = x^3) ---
p1 = getPrime(48)
a1 = 0
b1 = 0
t = randint(1, p1 - 1)
G1 = (pow(t, 2, p1), pow(t, 3, p1))
d = randint(1, p1 - 1)
t_G1 = G1[0] * pow(G1[1], -1, p1) % p1
t_Q1 = (d * t_G1) % p1
# t_Q1 == 0 の場合は無限遠点となり計算が失敗するため、再生成する
while t_Q1 == 0:
    d = randint(1, p1 - 1)
    t_Q1 = (d * t_G1) % p1
inv_t_Q1 = pow(t_Q1, -1, p1)
Q1 = (pow(inv_t_Q1, 2, p1), pow(inv_t_Q1, 3, p1))

# --- Curve 2 (安全な非特異曲線) ---
while True:
    p1_temp = getPrime(48)
    p2_temp = 2 * p1_temp + 1
    if p2_temp % 4 == 3 and isPrime(p2_temp):
        p2 = p2_temp
        break
while True:
    a2 = randint(1, p2 - 1)
    b2 = randint(1, p2 - 1)
    if (4 * a2**3 + 27 * b2**2) % p2 != 0:
        break
while True:
    x = randint(1, p2 - 1)
    y = get_y(x, a2, b2, p2)
    if y is not None:
        G2 = (x, y)
        break
Q2 = ec_mul(G2, d, a2, p2)

flag = b"E4syCTF{s1n8ul4r_curv3_1s_e4sy_t0_br3ak}"
m_int = int.from_bytes(flag, "big")
Px = Q2[0]
cipher = m_int ^ Px

print("\n" + "="*20)
print("       Curve 1")
print("="*20)
print(f"p={p1}")
print(f"a={a1}")
print(f"b={b1}")
print(f"G={G1}")
print(f"Q={Q1}")

print("\n" + "="*20)
print("       Curve 2")
print("="*20)
print(f"p={p2}")
print(f"a={a2}")
print(f"b={b2}")
print(f"G={G2}")
print(f"Q={Q2}")

print("\n" + "="*20)
print("       Cipher")
print("="*20)
print(f"cipher={cipher}\n")