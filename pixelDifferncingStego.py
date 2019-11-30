import os
import math
import numpy as np
import binascii
from PIL import Image
#from Crypto.Cipher import AES
#import cv2


def AES_encrypt(plaintext):
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext


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
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


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
    return answer + 1


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
    for col in range(y):
        for row in range(0, x - 1, 2):
            if message_len > 0:
                pixel1 = list(im.getpixel((row, col)))
                pixel2 = list(im.getpixel((row + 1, col)))
                for k in range(3):
                    if message_len > 0:
                        # Calculate differences in adjacent pixel colors
                        p1 = pixel1[k]
                        p2 = pixel2[k]
                        d = dValue(p1, p2)

                        # Find quantization ranges for pixel differences
                        quant_ranges = find_quant_range(d)
                        n = nearest_square(d)
                        m = quant_ranges[2][0] if len(quant_ranges) > 2 else quant_ranges[1]

                        # Get next m bits of secret message and convert to decimal
                        message_to_hide = ""
                        if message_len >= m:
                            message_to_hide = message_as_bits[message_len - m: message_len]
                        else:
                            message_to_hide = message_as_bits[message_len - message_len: message_len]
                        message_to_hide = int(message_to_hide, 2)

                        # Initialize dprime
                        dprime = 0

                        if d >= 240:
                            dprime = message_to_hide & 240
                            pixel_vals = stegano(p1, p2, d, dprime)
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
                                    if l & message_to_hide == message_to_hide:
                                        dprime = l
                                        pixel_vals = stegano(p1, p2, d, dprime)
                                        pixel1[k] = pixel_vals[0]
                                        pixel2[k] = pixel_vals[1]
                                # dprime was not found in first range, so check second range
                                if dprime == 0:
                                    # We now use the other m value
                                    m = quant_ranges[2][1]
                                    message_to_hide = message_as_bits[message_len - m: message_len]
                                    message_to_hide = int(message_to_hide, 2)
                                    quant_range = quant_ranges[1]
                                    num1 = quant_range[0]
                                    num2 = quant_range[1]
                                    for l in range(num1, num2 + 1):
                                        if l & message_to_hide == message_to_hide:
                                            dprime = l
                                            pixel_vals = stegano(p1, p2, d, dprime)
                                            pixel1[k] = pixel_vals[0]
                                            pixel2[k] = pixel_vals[1]
                            else:
                                # Must loop through values p in the only sub range to find a pi whose m LSBs == m bits of Secret message
                                for l in range(num1, num2 + 1):
                                    if l & message_to_hide == message_to_hide:
                                        dprime = l
                                        pixel_vals = stegano(p1, p2, d, dprime)
                                        pixel1[k] = pixel_vals[0]
                                        pixel2[k] = pixel_vals[1]
                        # Confirms that m bits have been successfully hidden
                        message_len -= m
                # Insert new pixel values
                im.putpixel((row, col), tuple(pixel1))
                im.putpixel((row, col + 1), tuple(pixel2))
                # Update location of last insert
                last_row = row + 1
                last_col = col
    return last_row, last_col


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
// Takes an image with a secret message and decodes it
// 
// @param   img_name   Relative file path to image
// @param   end_pixel   Last pixel to contain the secret message
//
// @return  ciphertext   Ciphertext of secret hidden message
'''
def extract_msg(img_name, end_pixel):
    im = Image.open(img_name, 'r')
    last_row = end_pixel[0]
    last_col = end_pixel[1]
    extracted_msg = ""
    for col in range(last_col+1):
        for row in range(0, last_row+1, 2):
                pixel1 = im.getpixel((row, col))
                pixel2 = im.getpixel((row + 1, col))
                for k in range(3):
                    # Calculate differences in adjacent pixel colors
                    p1 = pixel1[k]
                    p2 = pixel2[k]
                    d = dValue(p1, p2)

                    # Find quantization ranges for pixel differences
                    quant_ranges = find_quant_range(d)
                    m = quant_ranges[2][0] if len(quant_ranges) > 2 else quant_ranges[1]

                    # Initialize d
                    dprime = 0

                    if d >= 240:
                        # Converts integer to binary string
                        dprime = "{0:b}".format(d)
                        length = len(dprime)
                        extracted_msg = dprime[length - 4: length] + extracted_msg
                    # Must find dprime
                    else:
                        quant_range = quant_ranges[0]
                        num1 = quant_range[0]
                        num2 = quant_range[1]
                        if len(quant_ranges) > 2:
                            # Must loop through values p in the first sub range to find a pi whose m+1 LSBs = m+1 bits of Secret message
                            val = get_last_m_bits(d, m)
                            for l in range(num1, num2 + 1):
                                if l & val == val:
                                    dprime = l
                                    dprime = "{0:b}".format(dprime)
                                    length = len(dprime)
                                    extracted_msg = dprime[length - m: length] + extracted_msg
                            # dprime was not found in first range, so check second range
                            if dprime == 0:
                                # We now use the other m value
                                m = quant_ranges[2][1]
                                quant_range = quant_ranges[1]
                                num1 = quant_range[0]
                                num2 = quant_range[1]
                                val = get_last_m_bits(d, m)
                                for l in range(num1, num2 + 1):
                                    if l & val == val:
                                        dprime = l
                                        dprime = "{0:b}".format(dprime)
                                        length = len(dprime)
                                        extracted_msg = dprime[length - m: length] + extracted_msg
                        else:
                            # Must loop through values p in the only sub range to find a pi whose m LSBs == m bits of d
                            val = get_last_m_bits(d, m)
                            for l in range(num1, num2 + 1):
                                if l & val == val:
                                    dprime = l
                                    dprime = "{0:b}".format(dprime)
                                    length = len(dprime)
                                    extracted_msg = dprime[length - m: length] + extracted_msg
    return extracted_msg

print(string_to_binary("hello"))
binary = string_to_binary("hello")
pixel_loc = insert_msg("../city.png", binary)

print(extract_msg("../city.png", pixel_loc))
