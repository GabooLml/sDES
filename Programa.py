'''
Codigo que cifra mediante el uso de sDES
Antonio Roblero Alejandro Jesús
Rojas Mendez Gabriel
'''
import fileinput

lines = []
for line in fileinput.input(encoding="utf-8"):
    lines.append(line)

e = str.strip(lines[0])
key_e = str.strip(lines[1])
plaintext_e = str.strip(lines[2])

key = []
plaintext = []

def fill_array(n):
    array = []
    for i in range(0, n):
        array.append(0)
    return array

for i in range(0, len(key_e)):
    key.append(int(key_e[i]))

for i in range(0, len(plaintext_e)):
    plaintext.append(int(plaintext_e[i]))

P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

key1 = fill_array(8)
key2 = fill_array(8)

IP = [2, 6, 3, 1, 4, 8, 5, 7]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]

S0 = [[1, 0, 3, 2 ],
	  [3, 2, 1, 0 ],
	  [0, 2, 1, 3 ],
	  [3, 1, 3, 2 ]]

S1 = [[0, 1, 2, 3 ],
	  [2, 0, 1, 3 ],
	  [3, 0, 1, 0 ],
	  [2, 1, 0, 3 ]]

def shift(array, n):
    while n > 0:
        tmp = array[0]
        for i in range(0, len(array)-1):
            array[i] = array[i + 1]
        array[len(array)- 1] = tmp
        n -= 1
    return array

def key_generation():
    key_tmp = fill_array(10)
    Ls = fill_array(5)
    Rs = fill_array(5)

    for i in range(0, 10):
        key_tmp[i] = key[P10[i] - 1]

    for i in range(0, 5):
        Ls[i] = key_tmp[i]
        Rs[i] = key_tmp[i + 5]

    Ls_1 = shift(Ls, 1)
    Rs_1 = shift(Rs, 1)

    for i in range(0, 5):
        key_tmp[i] = Ls_1[i]
        key_tmp[i + 5] = Rs_1[i]

    for i in range(0, 8):
        key1[i] = key_tmp[P8[i] - 1]

    Ls_2 = shift(Ls, 2)
    Rs_2 = shift(Rs, 2)

    for i in range(0, 5):
        key_tmp[i] = Ls_2[i]
        key_tmp[i + 5] = Rs_2[i]

    for i in range(0, 8):
        key2[i] = key_tmp[P8[i] - 1]

def int_to_binary(val):
    if val == 0:
        return "00"
    elif val == 1:
        return "01"
    elif val == 2:
        return "10"
    else:
        return "11" 

def functions(array, key_tmp):
    l = fill_array(4)
    r = fill_array(4)
    ep = fill_array(8)
    l_1 = fill_array(4)
    r_1 = fill_array(4)

    for i in range(0, 4):
        l[i] = array[i]
        r[i] = array[i + 4]
    
    for i in range(0, 8):
        ep[i] = r[EP[i] - 1]
    
    for i in range(0, 8):
        array[i] = key_tmp[i] ^ ep[i]
    
    for i in range(0, 4):
        l_1[i] = array[i]
        r_1[i] = array[i + 4]

    row = int(format(int(str(l_1[0])+str(l_1[3])), 'd'), 2)
    col =  int(format(int(str(l_1[1])+str(l_1[2])), 'd'), 2)
    str_l = int_to_binary(S0[row][col])
    row = int(format(int(str(r_1[0])+str(r_1[3])), 'd'), 2)
    col =  int(format(int(str(r_1[1])+str(r_1[2])), 'd'), 2)
    str_r = int_to_binary(S1[row][col])

    r_tmp = fill_array(4)
    for i in range(0, 2):
        c1 = str_l[i]
        c2 = str_r[i]
        r_tmp[i] = int(c1)
        r_tmp[i+2] = int(c2)
    
    r_tmpP4 = fill_array(4)
    for i in range(0, 4):
        r_tmpP4[i] = r_tmp[P4[i] - 1]
    
    for i in range(0, 4):
        l[i] = l[i] ^ r_tmpP4[i]

    output = fill_array(8)
    for i in range(0, 4):
        output[i] = l[i]
        output[i + 4] = r[i]
    
    return output

def swap(array, n):
    l = fill_array(n)
    r = fill_array(n)
    output = fill_array(2*n)

    for i in range(0, n):
        l[i] = array[i]
        r[i] = array[i+n]
    
    for i in range(0, n):
        output[i] = r[i]
        output[i+n] = l[i]

    return output

def encryption(plaintext):
    array = fill_array(8)
    ciphertext = fill_array(8)
    
    for i in range(0, 8):
        array[i] = plaintext[IP[i] - 1]

    array1 = functions(array, key1)
    afterSwap = swap(array1, int(len(array1)/2))
    array2 = functions(afterSwap, key2)

    for i in range(0, 8):
        ciphertext[i] = array2[IP_inv[i] - 1]

    return ciphertext

def decryption(array):
    array_tmp = fill_array(8)
    decrypted = fill_array(8)

    for i in range(0, 8):
        array_tmp[i] = array[IP[i] - 1]

    array1 = functions(array_tmp, key2)
    after_swap = swap(array1, int(len(array)/2))
    array2 = functions(after_swap, key1)

    for i in range(0, 8):
        decrypted[i] = array2[IP_inv[i] - 1]
    
    return decrypted

key_generation()

if "E" == e:
    print("".join(str(i) for i in encryption(plaintext)))
else:
    key_generation()
    print("".join(str(i) for i in decryption(plaintext)))