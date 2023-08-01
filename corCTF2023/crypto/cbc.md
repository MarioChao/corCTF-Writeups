# Introduction

CBC is a type of cipher known as "cipher-block chaining".<br>
In this CTF, cbc provides you with a program and an output to decrypt the flag.<br>

## crypto/cbc

### Challenge Description:

who on earth is putting CLASSICAL BORING CRYPTOGRAPHY in my ctf

Downloads<br>
[cbc.py](https://static.cor.team/uploads/b34e0f3a8f593c51dc28844decc71e2a37a3e6316aa763853aed394d4602e17c/cbc.py) &nbsp; [cbc_output.txt](https://static.cor.team/uploads/5e93945f70c7b38bb7fca87cf7be309d0f7fd3ea7899b52c152b8094b714290b/cbc_output.txt)

### Solution:

#### -=[ First Step ]=-

Examine _cbc.py_

The alphabet is defined as all uppercase letters, and $bs$ (block size) is defined as 16.
```python
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16
```

The program opens up two text files the combines the alphabets in _message.txt_ with the content of _flag.txt_.
```python
message = open("message.txt").read().upper()
message = "".join([char for char in message if char in alphabet])
flag = open("flag.txt").read()
flag = flag.lstrip("corctf{").rstrip("}")
message += flag
assert all([char in alphabet for char in message])
```

Note that $alphabet$ contains only uppercase letters, so the `assert` confirms that all of the characters in $message$ are uppercase letters, and the $flag$ text that is directly concatenated to $message$ is also solely consisted of uppercase letters.

$key$ is assigned a string of random characters from $alphabet$ of length $bs$.
```python
def random_alphastring(size):
    return "".join(random.choices(alphabet, k=size))
# ...
key = random_alphastring(bs)
```

`add_key()` is defined to return the string $block$ with each character shifted cyclically right by the corresponding character of $key$ from its position in $alphabet$.<br>
In terms of popular ciphers, the function is a same-length Vigenere cipher that returns the Vigenere encryption of $block$ with the key $key$.
```python
def add_key(key, block):
    ct_idxs = [(k_a + pt_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])
```

`pad()` is defined to return the string $plaintext$ padded with `X` to the closest not-smaller-than multiple of $block\_size$.
```python
def pad(block_size, plaintext):
    plaintext += "X" * (-len(plaintext) % block_size)
    return plaintext
```

`cbc()` is defined to perform cipher-block chaining using the given $plaintext$ and $key$.<br>
First, it separates $plaintext$ into the variables $blocks$ with blocks of 16 characters, with the last block padded with `X`.<br>
Second, it generates a random $iv$ that is assigned to $prev\_block$.<br>
Third, the function goes through each block and performs some `add_key()` and concatenating $prev\_block$.<br>
The ciphertext is obtained from the concatenation of all $prev\_block$\'s.
```python
def cbc(key, plaintext):
    klen = len(key)
    plaintext = pad(klen, plaintext)
    iv = random_alphastring(klen)
    blocks = [plaintext[i:i+klen] for i in range(0, len(plaintext), klen)]
    prev_block = iv
    ciphertext = ""
    for block in blocks:
        block = add_key(prev_block, block)
        prev_block = add_key(key, block)
        ciphertext += prev_block
    return iv, ciphertext
```

$iv$ (initial vector) and $ct$ (ciphertext) from the cipher-block chain (cbc) function are printed out in the console.
```python
iv, ct = cbc(key, pad(bs, message))
print(f"{iv = }")
print(f"{ct = }")
```

---

#### -=[ Next Step ]=-

We will need to find a way to recover the original $plaintext$.

Recall from the _First_ step that $ct$ (ciphertext) is obtained by the concatenation of all $prev\_block$\'s.<br>
Therefore, we can get each $prev\_block$ by splitting $ct$ into groups of 16, and assign it to an array called $prev\_blocks$.
```python
prev_blocks = [ct[i : i + klen] for i in range(0, len(ct), klen)]
```

By listing out how $prev\_block$ updates in `cbc()`, you can see that $prev\_block$ changes each time by performing `add_key()` with the current $block$ and the $key$: (`a + b` denotes `add_key(b, a)`)
```python
# Block 1:
# block = block1 + prev_block
# prev_block = block + key = block1 + prev_block + key

# Block 2:
# block = block2 + prev_block
# prev_block = block + key = block2 + prev_block + key

# Block 3:
# block = block3 + prev_block
# prev_block = block + key = block3 + prev_block + key

# ...
```

Let's change it to 0-indexed and also index the $prev\_block$\'s according to our array $prev\_blocks$: (note that $prev\_block$ is initially $iv$)
```python
# Block 0:
# block = block0 + iv
# prev_block0 = block + key = block0 + iv + key

# Block 1:
# block = block1 + prev_block0
# prev_block1 = block + key = block1 + prev_block0 + key

# Block 2:
# block = block2 + prev_block1
# prev_block2 = block + key = block2 + prev_block1 + key

# ...
```

By reversing the process of `add_key()` on each $prev\_block$ using the previous $prev\_block$, we can get:
```python
# prev_block0 = block0 + iv + key
# prev_block1 = block1 + prev_block0 + key
# prev_block2 = block2 + prev_block1 + key

# Reverse add_key() on the previous prev_block
# prev_block0 - iv          = block0 + key
# prev_block1 - prev_block0 = block1 + key
# prev_block2 - prev_block1 = block2 + key
```

Also recall from the _First_ step that $plaintext$ is split into blocks of a fix length of 16.<br>
If each $block$ is added with the $key$ as shown above, then the concatenated string of every block will be the $plaintext$ encrypted with a 16-letter Vigenere key.<br>
The simplest solution for me to get the key is through [dcode.fr](https://www.dcode.fr)'s Vigenere decoder with key length of 16.

Since the "key length" option of the decoder has a size limit of 500, we can copy the $key$ and then use the "known key" option of the decoder to obtain the full $plaintext$.

---

#### -=[ Solve ]=-

Using the ideas from the _Next_ step, we can write a program that give us the Vigenere ciphertext.

First, define the reverse of `add_key()`, name it `remove_key()`.<br>
Basically, it is `add_key()` but with `(k_a + pt_a)` changed to `pt_a - k_a`.
```python
def remove_key(key, block):
    ct_idxs = [(pt_a - k_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])
```

Next, assign variables $iv$ and $ct$ using _cbc_output.txt_

```python
iv = "RLNZXWHLULXRLTNP"
ct = "ZQTJIHLVWMPBYIFRQBUBUESOOVCJHXXLXDKPBQCUXWGJDHJPQTHXFQIQMBXNVOIPJBRHJQOMBMNJSYCRAHQBPBSMMJWJKTPRAUYZVZTHKTPUAPGAIJPMZZZDZYGDTKFLWAQTSKASXNDRRQQDJVBREUXFULWGNSIINOYULFXLDNMGWWVSCEIORQESVPFNMWZKPIYMYVFHTSRDJWQBTWHCURSBPUKKPWIGXERMPXCHSZKYMFLPIAHKTXOROOJHUCSGINWYEILFIZUSNRVRBHVCJPVPSEGUSYOAMXKSUKSWSOJTYYCMEHEUNPJAYXXJWESEWNSCXBPCCIZNGOVFRTGKYHVSZYFNRDOVPNWEDDJYITHJUBVMWDNNNZCLIPOSFLNDDWYXMYVCEOHZSNDUXPIBKUJIJEYOETXWOJNFQAHQOVTRRXDCGHSYNDYMYWVGKCCYOBDTZZEQQEFGSPJJIAAWVDXFGPJKQJCZMTPMFZDVRMEGMPUEMOUVGJXXBRFCCCRVTUXYTTORMSQBLZUEHLYRNJAAIVCRFSHLLPOANFKGRWBYVSOBLCTDAUDVMMHYSYCDZTBXTDARWRTAFTCVSDRVEENLHOHWBOPYLMSDVOZRLENWEKGAWWCNLOKMKFWWAZJJPFDSVUJFCODFYIMZNZTMAFJHNLNMRMLQRTJJXJCLMQZMOFOGFPXBUTOBXUCWMORVUIIXELTVIYBLPEKKOXYUBNQONZLPMGWMGRZXNNJBUWBEFNVXUIAEGYKQSLYSDTGWODRMDBHKCJVWBNJFTNHEWGOZFEZMTRBLHCMHIFLDLORMVMOOHGXJQIIYHZFMROGUUOMXBTFMKERCTYXFIHVNFWWIUFTGLCKPJRFDRWDXIKLJJLNTWNQIOFWSIUQXMFFVIIUCDEDFEJNLKLQBALRKEYWSHESUJJXSHYWNRNPXCFUEFRJKSIGXHFTKNJXSYVITDOGYIKGJIOOHUFILWYRBTCQPRPNOKFKROTFZNOCZXZEYUNWJZDPJDGIZLWBBDGZJNRQRPFFGOTGFBACCRKLAPFLOGVYFXVIIJMBBMXWJGLPOQQHMNBCINRGZRBVSMLKOAFGYRUDOPCCULRBE"
```

Then, split $ct$ into $prev\_blocks$.
```python
klen = len(iv)
blockCnt = len(ct) // klen
prev_blocks = [ct[i : i + klen] for i in range(0, len(ct), klen)]
```

Afterwards, minus each $prev\_block$ by the previous $prev\_block$ to get $blocksAddKey$: (first $prev\_block$ will be subtracted by $iv$)
```python
blocksAddKey = [remove_key(prev_blocks[i - 1] if i > 0 else iv, prev_blocks[i]) for i in range(0, blockCnt)]
```

Concatenate the strings of the array to get the Vigenere ciphertext.
```python
code = "".join(blocksAddKey)
print("Code:", code)
```

Using [dcode.fr's Vigenere cipher](https://www.dcode.fr/vigenere-cipher), we obtain the key `ACXQTSTCSXZWFCZY`.

Decoding the full Vigenere ciphertext with the key gives us a large chunk of text, and the flag's text is located at the end.<br>
[Here](../../assets/corctf23_cbc_decrypted_text.txt) is the full decrypted text with spacing.

---

Flag: `corctf{ATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS}`

## Other Things

Here is a solution program to the challenge, I guess.<br>
[corctf23_cbc.py](../../assets/corctf23_cbc.py)