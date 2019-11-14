# @author Dylan Chow
# 
# These are the steps for inputting to the image
#
# 1. Find the difference of the image greyscale pixels d
#       d = |p(i) - p(i+1)|
# 2. Find the nearest square to the d value using the quanization range table
# 3. If d >= 240
#       d' = 240 + secret(msg)
#    If d < 240
#       *Check length of Array with subrange and m values
#       *If length = 2, then only one subrange if length > 2, then two subranges
#       If secret(msg length + 1) = LSB(p, m+1) //p is first subrange 
#           d' = p
#       else
#           If secret(msg length) = LSB(p', m) //p' is second subrange
#               d' = p

def dValue (pixel1, pixel2):
    dval = abs(pixel1 - pixel2)
    return (dval)
    
def compareBits(a, b, numOfBits):
    binStr_a = integerToBinaryStr(a)
    binStr_b = integerToBinaryStr(b)
    
    if(binStr_a[numOfBits:] == binStr_b[numOfBits:]):
        #print(binStr_a[numOfBits:] + " " + binStr_b[numOfBits:] + " true")
        return True
    #print(binStr_a[numOfBits:] + " " + binStr_b[numOfBits:] + " false")
    return False

def integerToBinaryStr(i):
    if i == 0:
        return "00000000"
    s = ''
    while i:
        if i & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        i //= 2

    if len(s) < 8:
        end = abs(len(s) - 8)
        t = ''
        for x in range(0, end):         
            t = "0" + t      
    return t + s

def stegano(pixel1, pixel2, d, dprime):
    if pixel1 >= pixel2 and dprime > d:
        steg1 = pixel1 + (abs(dprime - d)//2)
        steg2 = pixel2 - (abs(dprime - d)//2)
        #print("if statement 1")
        return (steg1, steg2)
    if pixel1 < pixel2 and dprime > d:
        steg1 = pixel1 - (abs(dprime - d)//2)
        steg2 = pixel2 + (abs(dprime - d)//2)
        #print("if statement 2")
        return (steg1, steg2)
    if pixel1 >= pixel2 and dprime <= d:
        steg1 = pixel1 - (abs(dprime - d)//2)
        steg2 = pixel2 + (abs(dprime - d)//2)
        #print("if statement 3")
        return (steg1, steg2)
    if pixel1 < pixel2 and dprime <= d:
        steg1 = pixel1 + (abs(dprime - d)//2)
        steg2 = pixel2 - (abs(dprime - d)//2)
        #print("if statement 4")
        return (steg1, steg2)
    return


def insertMsg (d, quantarray, n, secretmsg, p1, p2):
    secretm = int(secretmsg)
    if d >= 240:
        dprime = secretm & d
        print("D value is bigger than 240. dprime: " + dprime)
        return stegano(p1, p2, dorg, dprime)
    
    if d < 240:
        if len(quantarray) > 2:
            mrange = quantarray[2]
            m = mrange[0]
        else:
            m = quantarray[1]        

    if m == len(secretmsg):   
        subrange = quantarray[0]
        for item in range(subrange[0], subrange[1]+1):
            #print(item)
            if compareBits(item, secretm, 4):
                dprime = item
                print("subrange 1 used. dprime: " + str(dprime))
                return stegano(p1, p2, dorg, dprime)
    else:
        subrange = quantarray[1]
        for item in range(subrange[0], subrange[1]+1): 
            #print(item)
            if compareBits(item, secretm, 5):
                dprime = item
                print("subrange 2 used. dprime: " + str(dprime))
                return stegano(p1, p2, dorg, dprime)
    return -1

quant_range = [(30, 33), (34, 41), (4,3)]
#quant_range = [(30, 33), 4]
n = 6
secretmsg = "001"
pixel1 = 47
pixel2 = 81
dorg = dValue(pixel1, pixel2)
print("D: " + str(dorg))
print("n: " + str(n))
print("Secret msg: " + secretmsg)
#compareBits(32, 0, 4)
dprime = insertMsg(dorg, quant_range, n, secretmsg, pixel1, pixel2) 
print("New pair of pixels: " + str(dprime))