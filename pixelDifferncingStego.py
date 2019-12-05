import math
from PIL import Image
import re

# Python code to implement
# Vigenere Cipher
# Found on geeksforgeeks.com

# This function generates the
# key in a cyclic manner until
# it's length isn't equal to
# the length of original text
def generateKey(string, key):
    key = list(re.sub('[^A-Za-z0-9]+', '', key.upper()))
    if len(string) == len(key):
        return key
    else:
        for i in range(len(string) -
                       len(key)):
            key.append(key[i % len(key)])
    return "".join(key)


# This function returns the
# encrypted text generated
# with the help of the key
def cipherText(string, key):
    string = re.sub('[^A-Za-z0-9]+', '', string.upper())
    cipher_text = []
    for i in range(len(string)):
        x = (ord(string[i]) +
             ord(key[i])) % 26
        x += ord('A')
        cipher_text.append(chr(x))
    return "".join(cipher_text)


# This function decrypts the
# encrypted text and returns
# the original text
def originalText(cipher_text, key):
    orig_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 26) % 26
        x += ord('A')
        orig_text.append(chr(x))
    return "".join(orig_text)


'''
// Converts a string to a binary string
//
// @param   ciphertext    Text to be converted to binary
// @return  string   Binary equivalent as a string
'''
def string_to_binary(ciphertext):
    binary = bin(int.from_bytes(ciphertext.encode(), 'big'))
    return binary[:1] + binary[2:]


'''
// Converts a string of binary digits to its string equivalent
//
// @param   binaryCipher    
// @return  string representation of binary
'''
def binary_to_string(binaryCipher):
    n = int(binaryCipher, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(errors='replace')

'''
// Takes absolute difference of two numbers. Used to find diff in pixel vals
//
// @param   pixel1  First integer   
// @param   pixel2  Second integer    
//
// @return  dval Absolute difference of two pixel vals
'''
def dValue(pixel1, pixel2):
    dval = abs(pixel1 - pixel2)
    return (dval)


'''
// Calculates the nearest square number
// 
// @param   num Any number
// @return  square root of nearest square
'''
def nearest_square(num):
    answer = 0
    while ((answer+1)**2) < num:
        answer += 1
    diff1 = abs(num - answer**2)
    diff2 = abs(num - (answer+1)**2)
    if diff2 < diff1:
        answer += 1
    if diff2 - diff1 == 1:
        answer += 1
    return answer


'''
// Returns the last m bits of an integer
//
// @param   val     Integer input
// @param   num_bits    Number of bits to be returned
// @return  {integer}   Integer representation of m last bits
'''
def get_last_m_bits(val, num_bits):
    val = "{0:b}".format(val)
    length = len(val)
    val = val[length-num_bits: length]
    return int(val, 2)


'''
// Returns the row of the quantization range table
// 
// @param   d   Pixel difference d
// @return  array   Contains range(s) and m(s)
'''
def find_quant_range(d):
    # Obtain nearest square number of d
    n = nearest_square(d)
    range_width = 2*n

    # Find m
    m = math.floor(math.log2(range_width))
    two_power_m = math.pow(2, m)
    n_squared = n*n

    # Calculate quantization ranges
    if d < 256:
        if d < 240:
            if range_width > two_power_m:
                return [(n_squared - n, math.floor(n_squared + n - two_power_m) - 1),
                    (math.floor(n_squared + n - two_power_m), n_squared + n - 1), (m + 1, m)]

            else:
                return [(n_squared - n, n_squared + n - 1), m]
        else:
            return [(240, 255), 4]
    else:
        print("Invalid ")


'''
// Returns the new pixel values to be inserted into the picture
// 
// @param   pixel1   First pixel value
// @param   pixel2   Second pixel value
// @param   d        Pixel difference d
// @param   dprime   Calculated dprime value
//
// @return  {array}   Contains new pixel values
'''
def stegano(pixel1, pixel2, d, dprime):
    if (pixel1 >= pixel2 and dprime > d) or (pixel1 < pixel2 and dprime <= d):
        steg1 = pixel1 + math.ceil((abs(dprime - d) / 2))
        steg2 = pixel2 - (abs(dprime - d) // 2)
        # print("if statement 1")
        return steg1, steg2
    elif (pixel1 < pixel2 and dprime > d) or (pixel1 >= pixel2 and dprime <= d):
        steg1 = pixel1 - math.ceil((abs(dprime - d) / 2))
        steg2 = pixel2 + (abs(dprime - d) // 2)
        # print("if statement 2")
        return steg1, steg2
    return 0, 0


'''
// Takes a secret message as a binary string and hides it in the specified image
// 
// @param   img_name   Relative file path to image
// @param   message_as_bits   Message as string of bits
//
// @return  {array}   Pixel location of the end of the hidden message
'''
def insert_msg(img_name, message_as_bits):
    message_len = len(message_as_bits)
    im = Image.open(img_name, 'r')
    x, y = im.size
    last_row = 0
    last_col = 0
    for col in range(0, y - 1, 2):
        for row in range(x):
            if message_len > 0:
                pixel1 = list(im.getpixel((row, col)))
                pixel2 = list(im.getpixel((row, col + 1)))
                for k in range(3):
                    if message_len > 0:
                        # Calculate differences in adjacent pixel colors
                        p1 = pixel1[k]
                        p2 = pixel2[k]
                        d = dValue(p1, p2)
                        print("d: " + str(d))
                        # Find quantization ranges for pixel differences
                        quant_ranges = find_quant_range(d)
                        print("quant ranges: " + str(quant_ranges))
                        n = nearest_square(d)
                        m = quant_ranges[2][0] if len(quant_ranges) > 2 else quant_ranges[1]
                        print("m: " + str(m))
                        # Get next m bits of secret message and convert to decimal
                        message_to_hide = ""
                        if message_len >= m:
                            message_to_hide = message_as_bits[message_len - m: message_len]
                        else:
                            message_to_hide = message_as_bits[0: message_len]
                        if (len(message_to_hide) < m):
                            m = len(message_to_hide)
                        message_to_hide = int(message_to_hide, 2)

                        print("message to hide: " + str(message_to_hide))
                        # Initialize dprime
                        dprime = -1

                        if d >= 240:
                            dprime = message_to_hide & 240
                            print("dprime: " + str(dprime))
                            print("d: " + str(d))
                            print("p1: " + str(p1))
                            print("p2: " + str(p2))
                            pixel_vals = stegano(p1, p2, d, dprime)
                            print("k: " + str(k))
                            print("new pixel_vals: " + str(pixel_vals))
                            pixel1[k] = pixel_vals[0]
                            pixel2[k] = pixel_vals[1]
                        # Must find dprime
                        else:
                            quant_range = quant_ranges[0]
                            num1 = quant_range[0]
                            num2 = quant_range[1]
                            if len(quant_ranges) > 2:
                                # Must loop through values p in the first sub range to find a pi whose m+1 LSBs = m+1 bits of Secret message
                                for l in range(num1, num2 + 1):
                                    print("l: " + str(l))
                                    print("message_to_hide: " + str(message_to_hide))
                                    if get_last_m_bits(l, m) == get_last_m_bits(message_to_hide, m):
                                        dprime = l
                                        print("dprime: " + str(dprime))
                                        print("d: " + str(d))
                                        print("p1: " + str(p1))
                                        print("p2: " + str(p2))
                                        pixel_vals = stegano(p1, p2, d, dprime)
                                        print("k: " + str(k))
                                        print("new pixel_vals: " + str(pixel_vals))
                                        pixel1[k] = pixel_vals[0]
                                        pixel2[k] = pixel_vals[1]
                                        break
                                # dprime was not found in first range, so check second range
                                if dprime == -1:
                                    # We now use the other m value
                                    m = quant_ranges[2][1]
                                    start_index = message_len - m
                                    if start_index < 0:
                                        start_index = 0
                                    message_to_hide = message_as_bits[start_index: message_len]
                                    message_to_hide = int(message_to_hide, 2)
                                    quant_range = quant_ranges[1]
                                    num1 = quant_range[0]
                                    num2 = quant_range[1]
                                    for l in range(num1, num2 + 1):
                                        if get_last_m_bits(l, m) == get_last_m_bits(message_to_hide, m):
                                            dprime = l
                                            print("dprime: " + str(dprime))
                                            print("p1: " + str(p1))
                                            print("p2: " + str(p2))
                                            pixel_vals = stegano(p1, p2, d, dprime)
                                            print("k: " + str(k))
                                            print("new pixel_vals: " + str(pixel_vals))
                                            pixel1[k] = pixel_vals[0]
                                            pixel2[k] = pixel_vals[1]
                                            break
                            else:
                                # Must loop through values p in the only sub range to find a pi whose m LSBs == m bits of Secret message
                                for l in range(num1, num2 + 1):
                                    if get_last_m_bits(l, m) == get_last_m_bits(message_to_hide, m):
                                        dprime = l
                                        print("dprime: " + str(dprime))
                                        print("d: " + str(d))
                                        print("p1: " + str(p1))
                                        print("p2: " + str(p2))
                                        pixel_vals = stegano(p1, p2, d, dprime)
                                        print("k: " + str(k))
                                        print("new pixel_vals: " + str(pixel_vals))
                                        pixel1[k] = pixel_vals[0]
                                        pixel2[k] = pixel_vals[1]
                                        break
                        # Confirms that m bits have been successfully hidden
                        message_len -= m
                        print("Message left to hide: " + str(message_len))
                        print("----------------------------")
                # Insert new pixel values
                im.putpixel((row, col), tuple(pixel1))
                print("INSERTED NEW PIXEL " + str(pixel1) + " AT ROW " + str(row) + " AND COL " + str(col))
                im.putpixel((row, col + 1), tuple(pixel2))
                print("INSERTED 2ND NEW PIXEL " + str(pixel2) + " AT ROW " + str(row) + " AND COL " + str(col + 1))
                # Update location of last insert
                last_row = row
                last_col = col + 1
    im.save("city.png")
    return last_row, last_col


'''
// Takes an image with a secret message and decodes it
// 
// @param   img_name   Relative file path to image
// @param   end_pixel   Last pixel to contain the secret message
//
// @return  ciphertext   Ciphertext of secret hidden message
'''
def extract_msg(img_name, end_pixel):
    im = Image.open(img_name, 'r')
    x, y = im.size
    last_row = end_pixel[0]
    last_col = end_pixel[1]
    extracted_msg = ""
    print("------------EXTRACTION-------------")
    for col in range(0, last_col+1, 2):
        for row in range(x):
            if (row == last_row + 1) and (col + 1 == last_col):
                break
            print("Location: " + str(row) + ", " + str(col))
            pixel1 = im.getpixel((row, col))
            pixel2 = im.getpixel((row, col + 1))
            for k in range(3):
                # Calculate differences in adjacent pixel colors
                p1 = pixel1[k]
                p2 = pixel2[k]
                d = dValue(p1, p2)
                print("d: " + str(d))

                # Find quantization ranges for pixel differences
                quant_ranges = find_quant_range(d)
                m = quant_ranges[2][0] if len(quant_ranges) > 2 else quant_ranges[1]
                print("quant ranges: " + str(quant_ranges))
                print("m: " + str(m))

                # Initialize d
                dprime = -1

                if d >= 240:
                    # Converts integer to binary string
                    print("d: " + str(dprime))

                    dprime = "{0:b}".format(d)
                    print("dprime as bits: " + str(dprime))

                    length = len(dprime)
                    extracted_msg = dprime[length - 4: length] + extracted_msg
                    print(extracted_msg)
                # Must find dprime
                else:
                    quant_range = quant_ranges[0]
                    num1 = quant_range[0]
                    num2 = quant_range[1]
                    if len(quant_ranges) > 2:
                        # Must loop through values p in the first sub range to find a pi whose m+1 LSBs = m+1 bits of Secret message
                        val = get_last_m_bits(d, m)
                        for l in range(num1, num2 + 1):
                            if get_last_m_bits(l, m) == get_last_m_bits(val, m):
                                dprime = l
                                print("dprime: " + str(dprime))

                                dprime = "{0:b}".format(dprime)
                                print("dprime as bits: " + str(dprime))

                                length = len(dprime)
                                extracted_msg = dprime[length - m: length] + extracted_msg
                                print(extracted_msg)
                                break
                        # dprime was not found in first range, so check second range
                        if dprime == -1:
                            # We now use the other m value
                            m = quant_ranges[2][1]
                            quant_range = quant_ranges[1]
                            num1 = quant_range[0]
                            num2 = quant_range[1]
                            val = get_last_m_bits(d, m)
                            for l in range(num1, num2 + 1):
                                if get_last_m_bits(l, m) == get_last_m_bits(val, m):
                                    dprime = l
                                    print("dprime: " + str(dprime))

                                    dprime = "{0:b}".format(dprime)
                                    print("dprime as bits: " + str(dprime))

                                    length = len(dprime)
                                    extracted_msg = dprime[length - m: length] + extracted_msg
                                    print(extracted_msg)
                                    break
                    else:
                        # Must loop through values p in the only sub range to find a pi whose m LSBs == m bits of d
                        val = get_last_m_bits(d, m)
                        for l in range(num1, num2 + 1):
                            if get_last_m_bits(l, m) == get_last_m_bits(val, m):
                                dprime = l
                                print("dprime: " + str(dprime))

                                dprime = "{0:b}".format(dprime)
                                print("dprime as bits: " + str(dprime))

                                length = len(dprime)
                                extracted_msg = dprime[length - m: length] + extracted_msg
                                print(extracted_msg)
                                break
                print("k: " + str(k))
                print("----------------------")
    return extracted_msg


plaintext = "Cryptography is awesome!"
keyword = "MKONJIBHUVGHYCFT"
key = generateKey(plaintext, keyword)
cipher_text = cipherText(plaintext, key)
print(cipher_text)
print(originalText(cipher_text, key))

binary = string_to_binary(cipher_text)

pixel_loc = insert_msg("../city.png", binary)
print(originalText(binary_to_string(extract_msg("city.png", pixel_loc)), key))

