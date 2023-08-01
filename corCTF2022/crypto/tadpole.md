# Introduction

In this CTF, tadpole is a challenge based on decrypting a flag using the provided program and output.

## crypto/tadpole

### Challenge Description:

tadpoles only know the alphabet up to b... how will they ever know what p is?

Downloads<br>
[tadpole.py](https://static.cor.team/uploads/410646a89dc6c5f347fa3b576b4257e70fa58de60a4e50ba4b95ad208690f908/tadpole.py) &nbsp; [output.txt](https://static.cor.team/uploads/ddf6fc92767703c2a8f09d40cf3ef1a30c669a6e02efabae69027ca348b01ec7/output.txt)

### Solution:

{::options parse_block_html="true" /}

<details>

<summary>Solution</summary>

<details>

<summary>First</summary>

Examine the Python file _tadpole.py_

Three methods were imported at the start.
```python
from Crypto.Util.number import bytes_to_long, isPrime
from secrets import randbelow
```

The flag.txt content is converted from $bytes$ to $long$ and assigned to the variable $p$.<br>
The `assert` then tells us that $p$ is a prime number.
```python
p = bytes_to_long(open("flag.txt", "rb").read())
assert isPrime(p)
```

Two random numbers less than $p$ are assigned to $a$ and $b$.
```python
a = randbelow(p)
b = randbelow(p)
```

The function $f(s)$ is defined to change the parameter $s$ is some way and then return it.
```python
def f(s):
    return (a * s + b) % p
```

$a$ and $b$, along with two evaluations of $f(s)$, are printed at the end.
```python
print("a = ", a)
print("b = ", b)
print("f(31337) = ", f(31337))
print("f(f(31337)) = ", f(f(31337)))
```

</details>

<details>

<summary>Next</summary>

Before we start, write out the definition of the function $f(s)$.

$f(s) = (a \times s + b) \bmod p$

Next, we try to find a way to solve for $p$.<br>
Starting off with $f(31337)$.

1. Write $f(31337)$ in terms of $a$, $b$, and $p$:

    $(a \times 31337 + b) \bmod p = f(31337)$

2. The equation means that:

    $f(31337)$ is the remainder when $(a \times 31337 + b)$ is divided by $p$.

3. By subtracting the remainder from the dividend, the result will be divisible by the divisor: (assume $k$ is the quotient)

    $(a \times 31337 + b) - f(31337) = k \times p$

Then, moving on to $f(f(31337))$.

1. Similar to before, write $f(f(31337))$ in terms of $a$, $b$, and $p$, with $s = f(31337)$:

    $(a \times f(31337) + b) \bmod p = f(f(31337))$

2. Write it in terms of another multiple of $p$: (assume $l$ is the quotient)

    $(a \times f(31337) + b) - f(f(31337)) = l \times p$

Now, we have two equations with the left side solvable using information from _output.txt_

</details>

<details>

<summary>Solve</summary>

The two equations we got are:

$$
\begin{split}
(a \times 31337 + b) - f(31337) = k \times p \\
(a \times f(31337) + b) - f(f(31337)) = l \times p
\end{split}
$$

All variables on the left side are known in output.txt.

<details>

<summary>Output.txt</summary>

```
a =  7904681699700731398014734140051852539595806699214201704996640156917030632322659247608208994194840235514587046537148300460058962186080655943804500265088604049870276334033409850015651340974377752209566343260236095126079946537115705967909011471361527517536608234561184232228641232031445095605905800675590040729
b =  16276123569406561065481657801212560821090379741833362117064628294630146690975007397274564762071994252430611109538448562330994891595998956302505598671868738461167036849263008183930906881997588494441620076078667417828837239330797541019054284027314592321358909551790371565447129285494856611848340083448507929914
f(31337) =  52926479498929750044944450970022719277159248911867759992013481774911823190312079157541825423250020665153531167070545276398175787563829542933394906173782217836783565154742242903537987641141610732290449825336292689379131350316072955262065808081711030055841841406454441280215520187695501682433223390854051207100
f(f(31337)) =  65547980822717919074991147621216627925232640728803041128894527143789172030203362875900831296779973655308791371486165705460914922484808659375299900737148358509883361622225046840011907835671004704947767016613458301891561318029714351016012481309583866288472491239769813776978841785764693181622804797533665463949
```

</details>

<br>

Assign each number to a variable in the Python shell.

<details>

<summary>Assign Variables</summary>

```python
a =  7904681699700731398014734140051852539595806699214201704996640156917030632322659247608208994194840235514587046537148300460058962186080655943804500265088604049870276334033409850015651340974377752209566343260236095126079946537115705967909011471361527517536608234561184232228641232031445095605905800675590040729
b = 16276123569406561065481657801212560821090379741833362117064628294630146690975007397274564762071994252430611109538448562330994891595998956302505598671868738461167036849263008183930906881997588494441620076078667417828837239330797541019054284027314592321358909551790371565447129285494856611848340083448507929914
fs = 52926479498929750044944450970022719277159248911867759992013481774911823190312079157541825423250020665153531167070545276398175787563829542933394906173782217836783565154742242903537987641141610732290449825336292689379131350316072955262065808081711030055841841406454441280215520187695501682433223390854051207100
ffs = 65547980822717919074991147621216627925232640728803041128894527143789172030203362875900831296779973655308791371486165705460914922484808659375299900737148358509883361622225046840011907835671004704947767016613458301891561318029714351016012481309583866288472491239769813776978841785764693181622804797533665463949
```

</details>

<br>

After that, we just need to solve for $p$ using $k \times p$ and $l \times p$.

```python
kxp = (a * 31337 + b) - fs
lxp = (a * fs + b) - ffs
```

Since $p$ is a common factor of $k \times p$ and $l \times p$, we can get a multiple of $p$ equal to the greatest common denominator of the two values using Crypto's GCD function.

```python
from Crypto.Util.number import GCD
multP = GCD(kxp, lxp)
```

Luckily for us, this GCD is the prime $p$, and we can use Crypto's `long_to_bytes()` to get the flag.

```python
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(multP).decode("utf-8"))
# corctf{1n_m4th3m4t1c5,_th3_3ucl1d14n_4lg0r1thm_1s_4n_3ff1c13nt_m3th0d_f0r_c0mput1ng_th3_GCD_0f_tw0_1nt3g3rs} <- this is flag adm
```

</details>

<details>

<summary>Flag</summary>

flag: `corctf{1n_m4th3m4t1c5,_th3_3ucl1d14n_4lg0r1thm_1s_4n_3ff1c13nt_m3th0d_f0r_c0mput1ng_th3_GCD_0f_tw0_1nt3g3rs}`

</details>

</details>

{::options parse_block_html="false" /}

## Other Things:

This was my first Python challenge in a CTF contest, so when I opened tadpole.py, I didn't know what _Crypto_ and _secrets_ are.

I searched up these libraries and eventually used pip to install _Crypto_ in my Python.

During the contest, I didn't know the existence of GCD() in Python, so I instead used an online Big Number Calculator to get the GCD of the two big numbers.