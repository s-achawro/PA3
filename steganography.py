# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        try:
            image = cv2.imread(filein)
        except Exception as e:
            print("Error reading input image:", str(e))
            return
        #print(image) # for debugging
        
        # calculate available bytes
        try:
            max_bytes = image.shape[0] * image.shape[1] * 3 // 8
            print("Maximum bytes available:", max_bytes)
        except Exception as e:
            print("Error calculating available bytes:", str(e))
            return
        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()

        self.text = message
        self.binary = self.codec.encode(message+ self.delimiter)
        # check if possible to encode the message
        # number of bytes
        num_bytes = ceil(len(self.binary)//8) + 1 

        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            # your code goes here
            # you may create an additional method that modifies the image array

           
            binary = []
            for val in self.binary:
                binary.append(int(val))
            tempimage = image.flatten() #flatten the image array
            
            i = 0
            #iterate through each value on the tempimage array
            for j in range(len(tempimage)):
                if i > len(binary) - 1:
                    break
                # if the value is even and the binary value is 1, add 1 to the value
                if tempimage[j] % 2 == 0 and binary[i] == 1:
                    tempimage[j] += 1
                # if the value is odd and the binary value is 0, subtract 1 from the value
                elif tempimage[j] % 2 == 1 and binary[i] == 0:
                    tempimage[j] -= 1
                i += 1

            #unflatten the image array and save all the elmements from tempimage into image
            tempimage = np.reshape(tempimage, (image.shape[0], image.shape[1], image.shape[2]))
            image = tempimage
            #save the image to the fileout
            cv2.imwrite(fileout, image)
            
            
    def decode(self, filein, codec):
        try:
            image = cv2.imread(filein)
        except Exception as e:
            print("Error reading input image:", str(e))
            return
        #print(image) # for debugging
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            shift = int(input('Input Shift: '))
            self.codec = CaesarCypher(shift)
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        #you can't decode something unless it is binary
        
        if flag:
            # your code goes here
            # you may create an additional method that extract bits from the image array
            binary_msg = '' #flatten the image array

            tempimage = image.flatten()
            # iterate through each value in the tempimage array
            # decode the binary message
            for i in range(len(tempimage)):
                if tempimage[i] % 2 == 0:
                    binary_msg += '0'
                else:
                    binary_msg += '1'
                # if the binary message is a delimiter, stop decoding
                if self.delimiter in binary_msg:
                    break

                    
            # update the data attributes:
            self.text = self.codec.decode(binary_msg)
            binary_msg = self.cut_string(binary_msg, '00100011')
            self.binary = binary_msg

    def cut_string(self, string, delimiter):
        # Find the index of the delimiter in the string
        #divide the string into chunks of 8 characters
        for i in range(0, len(string), 8):
            #if the chunk matches the delimiter, return the chunk
            if string[i:i+8] == delimiter:
                return string[:i+8]

        # Otherwise, return the part of the string up to and including the delimiter
        return string[:delimiter_index + len(delimiter)]


    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()

    s.encode('redbox.jpg', 'alisfile.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    

    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')