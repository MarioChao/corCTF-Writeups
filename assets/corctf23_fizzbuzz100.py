# corCTF 2023 FizzBuzz100

from pwn import *
from Crypto.Util.number import *

rem = None
n = None
e = None
ct = None

def connect():
    global rem
    rem = remote("be.ax", 31100)

def disconnect():
    rem.close()

def getInput():
    global n
    global e
    global ct
    n = int(rem.recvline().strip()[3:]) # p * q
    e = int(rem.recvline().strip()[3:]) # encrypt code 65537
    ct = int(rem.recvline().strip()[4:]) # encrypted flag

def send(text):
    rem.recv()
    rem.sendline(bytes(text, "utf-8"))

def oracle(code):
    send(str(code))
    return rem.recvline().strip()

def solve():
    print(f"{n = }")
    print(f"{e = }")
    print(f"{ct = }")
    # Encrypt 2 to get 2^e % n
    c2 = pow(2, e, n)
    c2pt = oracle(c2).decode("utf-8")
    print(f"{c2pt = } (should be 2)")
    # Compute c2 * ct, or 2^e * flag^e % n = (2*flag)^e % n
    cHax = c2 * ct % n
    # Send (2*flag)^e % n to get (2*flag)^ed % n, or 2*flag
    print(f" {cHax = }")
    out = oracle(cHax).decode("utf-8")
    print(f"{out = }")
    if not out.isdigit():
        print("Fail!")
        return False
    print("Success!")
    out = int(out)
    # Divide 2 to get flag
    out //= 2
    # Print flag bytes
    print(" Flag:", getFlag(int(out)))
    return True

def getFlag(num):
    flag = long_to_bytes(num)[16:-16]
    return flag.decode("utf-8")

# Run until success
while True:
    connect()
    getInput()
    if solve():
        break
    disconnect()
