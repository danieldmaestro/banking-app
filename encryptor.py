nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", 
            "s", "t", "u", "v", "w", "x", "y", "z"]

def encryptor(text, key = 25):
    text_encrypt = ""
    for str in text:
        # check if character is a space and appends as is
        if str.isspace():
            text_encrypt += str
        # checks if char is a number and offsets it as needed
        elif str.isnumeric():
            n_index = nums.index(str) - (key % 10)
            text_encrypt += nums[n_index]
        # checks if char is an alphabet
        elif str.isalpha():
            # checks if alphabet is uppercase, swaps case and offsets accordingly
            if str.isupper():
                n_index = alphabets.index(str.lower()) - (key % 26)
                text_encrypt += alphabets[n_index]
            # checks if alphabet is lowercase, swaps case and offsets accordingly
            else:
                n_index = alphabets.index(str) - (key % 26)
                text_encrypt += alphabets[n_index].swapcase()
        # if character is any symbol, appends as is
        else:
            text_encrypt += str

    return text_encrypt