import math
import numpy as np
import binascii
#import cv2


'''
// Function to begin program (needs work)
'''
def embed_image_with_message(img, msg):
    img = cv2.imread(img)
    print(img.shape[0])


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
// Converts a string to binary as a string
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


print(find_quant_range(142))
print(binary_to_string(string_to_binary("rotjgn")))

#embed_image_with_message("Screen Shot 2019-10-07 at 10.12.36 PM.png")