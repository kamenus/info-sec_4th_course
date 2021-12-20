import hashlib
import random

def H(*args) -> int:
    """A one-way hash function."""
    a = ":".join(str(a) for a in args)
    return int(hashlib.sha256(a.encode("utf-8")).hexdigest(), 16)

def cryptrand(n: int = 1024):
    return random.SystemRandom().getrandbits(n) % N

# A large safe prime (N = 2q+1, where q is prime)
# All arithmetic is done modulo N
# (generated using "openssl dhparam -text 1024")
N = """00:9e:a9:ce:5a:8e:c7:5c:47:12:e0:4c:37:ad:c9:
       45:75:bf:5e:d6:a4:08:de:35:e6:33:75:7f:fa:fc:
       15:ac:12:e4:32:df:93:d7:c3:19:9c:ff:97:2e:29:
       49:6d:80:ba:e5:71:e5:ae:e8:54:7b:41:76:2a:68:
       a0:04:92:78:5c:9a:6d:fe:0d:a8:42:4b:27:06:6a:
       90:23:09:68:41:2c:f2:fa:56:4c:82:96:d5:3a:9d:
       60:5f:50:06:01:bb:3d:51:6d:57:f4:6d:f0:61:30:
       2a:84:8a:fe:3e:d9:d4:f7:b9:7d:d8:04:17:a4:42:
       bb:3e:8d:3b:f1:46:e9:37:53"""
     
N = int("".join(N.split()).replace(":", ""), 16)
g = 2  # A generator modulo N

k = H(N, g) # Multiplier parameter (k=3 in legacy SRP-6)

F = '#0x' # Format specifier

print("\n0. server stores (I, s, v) in its password database")

# The server must first generate the password verifier
I = "admin"         # Username
p = "nimda"         # Password
s = cryptrand(64)   # Salt for the user
x = H(s, I, p)      # Private key
v = pow(g, x, N)    # Password verifier

print(f'{I}\n{p}\n{s :{F}}\n{x :{F}}\n{v :{F}}')

print("\n1. client sends username I and public ephemeral value A to the server")
a = cryptrand()
A = pow(g, a, N)
print(f"{I}\n{A :{F}}")  # client->server (I, A)

print("\n2. server sends user's salt s and public ephemeral value B to client")
b = cryptrand()
B = (k * v + pow(g, b, N)) % N
print(f"{s :{F}}\n{B :{F}}")  # server->client (s, B)

print("\n3. client and server calculate the random scrambling parameter")
u = H(A, B)  # Random scrambling parameter
print(f"{u :{F}}")

print("\n4. client computes session key")
x = H(s, I, p)
S_c = pow(B - k * pow(g, x, N), a + u * x, N)
K_c = H(S_c)
print(f"{S_c :{F}}\n{K_c :{F}}")

print("\n5. server computes session key")
S_s = pow(A * pow(v, u, N), b, N)
K_s = H(S_s)
print(f"{S_s :{F}}\n{K_s :{F}}")

print("\n6. client sends proof of session key to server")
M_c = H(H(N) ^ H(g), H(I), s, A, B, K_c)
print(f"{M_c :{F}}")
# client->server (M_c) ; server verifies M_c

print("\n7. server sends proof of session key to client")
M_s = H(A, M_c, K_s)
print(f"{M_s :{F}}")
# server->client (M_s) ;  client verifies M_s
