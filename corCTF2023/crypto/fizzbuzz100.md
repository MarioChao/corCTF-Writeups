# Introduction

Fizzbuzz is a type of algorithm that usually prints out "Fizz" or "Buzz" if a number is divisible by 3 or 5 respectively, "Fizzbuzz", if the number is divisible by both 3 and 5, or the number itself if it's divisible by neither 3 nor 5.

In this challenge, the program runs an RSA encryption of a padded flag and provides an interaction that decrypts given numbers.

## crypto/fizzbuzz100

### Challenge Description:

lsb oracles are pretty overdone... anyway here's fizzbuzz

nc be.ax 31100

Downloads<br>
[fizzbuzz100.py](https://static.cor.team/uploads/e23d864efe7fa74f8c5a309f8c8b380e520242cdc62b817b10534dae40516d23/fizzbuzz100.py)

### Solution:

#### -=[ First ]=-

Notice that the interaction prints something as long as the $pt$ (plaintext) of the given $ct$ (ciphertext) isn't the padded flag.
```python
while True:
    ct = int(input("> "))
    pt = pow(ct, d, n)
    out = ""
    if pt == flag:
        exit(-1)
    if pt % 3 == 0:
        out += "Fizz"
    if pt % 5 == 0:
        out += "Buzz"
    if not out:
        out = pt
    print(out)
```

---

#### -=[ Next ]=-

We can make the interaction spit out a $pt$ closely related to the $flag$ by sending a $ct$ derived from the flag's ciphertext (let it be $flag\_ct$).

In this case, we will send $flag\_ct$ multiplied by $2^e \bmod n$, with $e$ as the RSA public key exponent and $n$ as the RSA public key modulo.
```python
cSend = (pow(2, e, n) * flag_ct) % n
```

To get how this works, note that $flag\_ct$ is computed in _fizzbuzz100.py_ as $flag^e \bmod n$.

Also note that $d$ (the RSA private key exponent) multiplied with $e$ in the exponent is 1 modulo n.<br>
This is an RSA key property.

```python
p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x10001
d = pow(e, -1, (p-1)*(q-1))
assert flag < n
ct = pow(flag, e, n)
```

When we multiply $flag\_ct$ with $2^e \bmod n$, we get:

$(flag\_ct \times 2^e \bmod n) \bmod n$<br>
$= (flag^e \times 2^e) \bmod n$<br>
$= (2 \times flag)^e \bmod n$

The server will decrypt this as $(2 \times flag)^{ed} \bmod n$, and because $ed$ in the exponent is 1, this is equal to $2 \times flag \bmod n$.<br>
The product is likely smaller than $n$, so we can assume the result is $2 \times n$.

The result $2 \times flag$ isn't equal to the padded flag $flag$, so it will be printed as long as it's not divisible by 3 or 5.

Thus, the padded flag can be obtained by dividing the server's response by 2 if it's numerical, and the flag can be retrieved using `long_to_bytes()`.

---

#### -=[ Solve ]=-

When you connect to the server, you will be given $n$, $e$, and $ct$.<br>
Copy and define them in a Python shell. (these values are examples)
```python
n = 119123668885405446943711690992484710880348016948446584070770707586054162937853924575762952780385856180974729827721835400650868675048266924139261228481610623948258834051196703425482676529264890896094641141458609240759620881837936691410922098296205309525259445956799199776139296928298136227781245860313475468893
e = 65537
ct = 65101200367832347089653988234979062049057812061829546386783041956646066234429980301943805741227019311465503947082490378114527855610574481752305150688689252075058873183600534911531211965075523624143612364415741492931803894181225640248235272060367779620218883268382636280541753000903752387734798144558258061914
```

Compute $\left( (2^e \bmod n) \times ct \right) \bmod n$:
```python
print((pow(2, e, n) * ct) % n)
# 54181182074761465466511121292413548214085470266318852508230308084611107159662214559137496522341502742348174993039462453924283525126178260757089231123970824685929405268053599888612016062135097434657623639619257163575193956754068216223573628096955130399706186950705988105594321564861126112976562314266847435301
```

Send the number to the server and hope it will respond with a number:
```python
# Server:
3510292330900880341740400801940023796904131039770746236285518800557729362649555991646114001355045852638976159945323744576456058127621476539047627817300398556173340686188190255702543934918930285369406397554013763287515129889968181372530463706787811163662423162652738340164810161642
```

Floor divide the number by 2 and run `long_to_bytes()`:
```python
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(3510292330900880341740400801940023796904131039770746236285518800557729362649555991646114001355045852638976159945323744576456058127621476539047627817300398556173340686188190255702543934918930285369406397554013763287515129889968181372530463706787811163662423162652738340164810161642 // 2))
```

The flag can be found in the middle of the string.

---

Flag: `corctf{h4ng_0n_th15_1s_3v3n_34s13r_th4n_4n_LSB_0r4cl3...4nyw4y_1snt_f1zzbuzz_s0_fun}`

</details>

</details>

## Other Things

### Figuring the Solution

I have no experience with RSA before, so I started out by searching up Least Significant Bit (LSB) oracles and implementing it.

That led to me deciding to use _pwntools_ because I heard that it can do automatic interactions with a server (I also didn't use _socket_ before).

However, downloading _pwntools_ was a very tough thing to do on my mac: I had to mix _pip_ and _brew_ commands and other parameters in order to download it into Python successfully.<br>
At the end, I only got it to work in the terminal using the _python3.10_ command.

Then, I made a ticket asking about how LSB works, and an organizer responded that LSB isn't relevant to fizzbuzz100.<br>
After a while, I only understood LSB with modulo 2, so I didn't bother deriving it with modulo 3 or 5 and other conditions (which is for fizzbuzz101).

I finally found the solution to the challenge through an article that was on LSB.

I found it from [this article](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-3/) in BitsDeep about LSB oracle. In that page, I decided to click on the "Part 1" button to look into RSA.<br>
As a result, I was able to find the solution at the section [Decipher Oracle](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-1/#:~:text=Decipher%20oracle).

That also introduced me to RSA.

### Floating Point Issue

Another issue I faced was to divide the returned value by a number.

In C++, getting an integer from an integer division only requires a slash, but in Python, any single-slash division results in a decimal.<br>
I decided to use `int(a / b)` for divisions because I thought that would round the quotient towards negative infinity.<br>
The truth is that with very big numbers, precision of the decimal will be lost and the resulting integer will have a significant difference than the actual quotient.

I finally found this issue when I got regular results (random characters) for `long_to_bytes()` on a number, but mostly the character `\x00` when using the number `int(num / 2)`.<br>
I searched up how to do floor divisions in Python and found the solution to this problem using double-slash `//`.

### Program

Here's a program to the challenge that automatically reconnects to the server until a potential flag is retrieved.<br>
[corctf23_fizzbuzz100.py](../../assets/corctf23_fizzbuzz100.py)
