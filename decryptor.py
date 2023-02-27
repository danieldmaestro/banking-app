nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", 
            "s", "t", "u", "v", "w", "x", "y", "z"]

def decryptor(text, key = 25):

    text_decrypt = ""
    for str in text:
        if str.isspace():
            text_decrypt += str
        elif str.isnumeric():
            n_index = (nums.index(str) + key) % 10
            text_decrypt += nums[n_index]
        elif str.isalpha():
            if str.isupper():
                index = alphabets.index(str.lower())
                n_index = (index + key) % 26
                text_decrypt += alphabets[n_index]
            else:
                index = alphabets.index(str)
                n_index = (index + key) % 26
                text_decrypt += alphabets[n_index].swapcase()

        else:
            text_decrypt += str
    
    return text_decrypt