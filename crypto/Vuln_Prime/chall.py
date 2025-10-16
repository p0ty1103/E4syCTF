import os
from Crypto.Util.number import getPrime, isPrime

FLAG = os.getenv("FLAG", "E4syCTF{Th1s_fl4g_i5_v3ry_vu1n3r4b13}").encode()
m = int.from_bytes(FLAG, 'big')

while True:
        p = getPrime(512)
        q = 2 * p + 1
        if isPrime(q):
                break

n = p * q
e = 65537
c = pow(m, e, n)

print(f"{n = }")
print(f"{c = }")