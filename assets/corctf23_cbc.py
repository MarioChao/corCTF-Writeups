# corCTF 2023 cbc

usingInput = False

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
bs = 16

def inputInfo():
    global iv
    global ct
    if usingInput:
        iv = input("iv: > ") # start point
        ct = input("ct: > ")
        bs = len(iv)
    else:
        iv = "RLNZXWHLULXRLTNP"
        ct = "ZQTJIHLVWMPBYIFRQBUBUESOOVCJHXXLXDKPBQCUXWGJDHJPQTHXFQIQMBXNVOIPJBRHJQOMBMNJSYCRAHQBPBSMMJWJKTPRAUYZVZTHKTPUAPGAIJPMZZZDZYGDTKFLWAQTSKASXNDRRQQDJVBREUXFULWGNSIINOYULFXLDNMGWWVSCEIORQESVPFNMWZKPIYMYVFHTSRDJWQBTWHCURSBPUKKPWIGXERMPXCHSZKYMFLPIAHKTXOROOJHUCSGINWYEILFIZUSNRVRBHVCJPVPSEGUSYOAMXKSUKSWSOJTYYCMEHEUNPJAYXXJWESEWNSCXBPCCIZNGOVFRTGKYHVSZYFNRDOVPNWEDDJYITHJUBVMWDNNNZCLIPOSFLNDDWYXMYVCEOHZSNDUXPIBKUJIJEYOETXWOJNFQAHQOVTRRXDCGHSYNDYMYWVGKCCYOBDTZZEQQEFGSPJJIAAWVDXFGPJKQJCZMTPMFZDVRMEGMPUEMOUVGJXXBRFCCCRVTUXYTTORMSQBLZUEHLYRNJAAIVCRFSHLLPOANFKGRWBYVSOBLCTDAUDVMMHYSYCDZTBXTDARWRTAFTCVSDRVEENLHOHWBOPYLMSDVOZRLENWEKGAWWCNLOKMKFWWAZJJPFDSVUJFCODFYIMZNZTMAFJHNLNMRMLQRTJJXJCLMQZMOFOGFPXBUTOBXUCWMORVUIIXELTVIYBLPEKKOXYUBNQONZLPMGWMGRZXNNJBUWBEFNVXUIAEGYKQSLYSDTGWODRMDBHKCJVWBNJFTNHEWGOZFEZMTRBLHCMHIFLDLORMVMOOHGXJQIIYHZFMROGUUOMXBTFMKERCTYXFIHVNFWWIUFTGLCKPJRFDRWDXIKLJJLNTWNQIOFWSIUQXMFFVIIUCDEDFEJNLKLQBALRKEYWSHESUJJXSHYWNRNPXCFUEFRJKSIGXHFTKNJXSYVITDOGYIKGJIOOHUFILWYRBTCQPRPNOKFKROTFZNOCZXZEYUNWJZDPJDGIZLWBBDGZJNRQRPFFGOTGFBACCRKLAPFLOGVYFXVIIJMBBMXWJGLPOQQHMNBCINRGZRBVSMLKOAFGYRUDOPCCULRBE"

def solve():
    klen = len(iv)
    blockCnt = len(ct) // klen
    # If 1-indexed:
    # cprev_block1 = iv + block1 + key
    # cprev_block2 = cprev_block1 + block2 + key
    # cprev_block3 = cprev_block2 + block3 + key
    # cprev_block4 = cprev_block3 + block4 + key

    # Divide ct into blocks
    cprev_blocks = [ct[i : i + klen] for i in range(0, len(ct), klen)]
    #print(cprev_blocks)
    
    # Calculate block + key for each block
    # block1 + key = cprev_block1 - iv
    # block2 + key = cprev_block2 - cprev_block1
    # block3 + key = cprev_block3 - cprev_block2
    blocksAddKey = [remove_key(cprev_blocks[i - 1] if i > 0 else iv, cprev_blocks[i]) for i in range(0, blockCnt)]
    #print(blocksAddKey)
    code = "".join(blocksAddKey)
    print("Code:", code)

    # Solve for key
    print()
    print("Use Vigenere Cipher for the code above with key length =", klen ,"to solve for the key")
    print("Possibly with https://www.dcode.fr/vigenere-cipher")
    key = None
    if not usingInput:
        key = "ACXQTSTCSXZWFCZY" # From dcode.fr
        print(f"{key = }")
    else:
        key = input("key: > ")

    # Decrypt text
    res = decryptVigenere(code, key)
    print()
    print("Res:", res)

def remove_key(key, block):
    ct_idxs = [(pt_a - k_a) % len(alphabet) for k_a, pt_a in zip([alphabet.index(k) for k in key], [alphabet.index(pt) for pt in block])]
    return "".join([alphabet[idx] for idx in ct_idxs])

def decryptVigenere(code, key):
    keyIdx = 0
    decrypt = ""
    for i in range(len(code)):
        isAlphabet = code[i].isalpha()
        if isAlphabet and code[i].isupper():
            charId = ord(code[i]) - ord('A')
            keyId = ord(key[keyIdx].lower()) - ord('a')
            decrypt += chr((charId - keyId) % 26 + ord('A'))
        elif isAlphabet and code[i].islower():
            charId = ord(code[i]) - ord('a')
            keyId = ord(key[keyIdx].lower()) - ord('a')
            decrypt += chr((charId - keyId) % 26 + ord('a'))
        else:
            decrypt += code[i]
            continue
        keyIdx = (keyIdx + 1) % len(key)
    return decrypt

if __name__ == "__main__":
    inputInfo()
    solve()

# Block 1:
# block = block1 + iv
# prev_block = block + key = block1 + iv + key

# Block 2:
# block = block2 + prev_block
# prev_block = block + key = block2 + prev_block + key

# Block 3:
# block = block3 + prev_block
# prev_block = block + key = block3 + prev_block + key

# Block 4:
# block = block4 + prev_block
# prev_block = block4 + prev_block + key

#IDJUSTLIKETOINTERJECTFORAMOMENTWHATYOUREREFERINGTOASLINUXISINFACTGNULINUXORASIVERECENTLYTAKENTOCALLINGITGNUPLUSLINUXLINUXISNOTANOPERATINGSYSTEMUNTOITSELFBUTRATHERANOTHERFREECOMPONENTOFAFULLYFUNCTIONINGGNUSYSTEMMADEUSEFULBYTHEGNUCORELIBSSHELLUTILITIESANDVITALSYSTEMCOMPONENTSCOMPRISINGAFULLOSASDEFINEDBYPOSIXMANYCOMPUTERUSERSRUNAMODIFIEDVERSIONOFTHEGNUSYSTEMEVERYDAYWITHOUTREALIZINGITTHROUGHAPECULIARTURNOFEVENTSTHEVERSIONOFGNUWHICHISWIDELYUSEDTODAYISOFTENCALLEDLINUXANDMANYOFITSUSERSARENOTAWARETHATITISBASICALLYTHEGNUSYSTEMDEVELOPEDBYTHEGNUPROJECTTHEREREALLYISALINUXANDTHESEPEOPLEAREUSINGITBUTITISJUSTAPARTOFTHESYSTEMTHEYUSELINUXISTHEKERNELTHEPROGRAMINTHESYSTEMTHATALLOCATESTHEMACHINESRESOURCESTOTHEOTHERPROGRAMSTHATYOURUNTHEKERNELISANESSENTIALPARTOFANOPERATINGSYSTEMBUTUSELESSBYITSELFITCANONLYFUNCTIONINTHECONTEXTOFACOMPLETEOPERATINGSYSTEMLINUXISNORMALLYUSEDINCOMBINATIONWITHTHEGNUOPERATINGSYSTEMTHEWHOLESYSTEMISBASICALLYGNUWITHLINUXADDEDORGNULINUXALLTHESOCALLEDLINUXDISTRIBUTIONSAREREALLYDISTRIBUTIONSOFGNULINUXANYWAYHERECOMESTHEFLAGITSEVERYTHINGAFTERTHISATLEASTITSNOTAGENERICROTTHIRTEENCHALLENGEIGUESS
