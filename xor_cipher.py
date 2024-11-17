#XOR Cipher - Yoni Danzig
#import modules
import itertools
import string

#program functions
def xor_decrypt(encrypted_text, key):
    """
    function takes an encrypted message (list on integers) and decrypt it according to the provided key.
    """
    # Convert the key to a list of ASCII codes
    key_codes = [ord(c) for c in key]
    # Decrypt each byte of the encrypted text using the key
    decrypted_bytes = [byte ^ key_codes[i % len(key_codes)] for i, byte in enumerate(encrypted_text)]
    # Convert the decrypted bytes to a string
    decrypted_text = ''.join([chr(byte) for byte in decrypted_bytes])
    return decrypted_text

def generate_keys(key_size, chars = string.ascii_lowercase):
    """
    function returns a list of all possible key combinations of all 26 low letters English alphabetic.
    amount of possible combination is len(chars) ** key_size
    """
    #The encryption key consists of key_size lower-case English characters - 'abcdefghijklmnopqrstuvwxyz' (26 letters)
    all_possible_combinations = itertools.product(chars, repeat=key_size) #Iterator with all possible combinations of chars
    return [''.join(key) for key in all_possible_combinations] #All possible combinations key result in a list

def guess_key_space_filter(encrypted_text, key_size, filter_result=True, spaces_th = 140):
    """
    function will return possible decrypt message according to spaces threshold.

    Args:
        encrypted_text: list of integers presenting encrypted message.
        key_size: An integer presenting the key size.
        filter_result: Boolean - True/False to use the space filter

    Returns:
        List of tuples. each tuple result has 2 values - (possible_key, decrypted_message)
    """
    possible_keys = []
    try:
        for key in generate_keys(key_size):
            decrypted_text = xor_decrypt(encrypted_text, key)
            if filter_result:
                if decrypted_text.count(" ") >= spaces_th:
                    possible_keys.append((key, decrypted_text))
            else:
                possible_keys.append((key, decrypted_text))
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    return possible_keys

def encrypted_textfile_to_list(filename):
    """
    function takes a text filename path that contains encrypted message separated by comma for ex: 26,35,67,89
    function returns the encrypted message as a list.
    """
    with open(filename, 'r') as f:
        encrypted_text = f.read().strip().split(',') #list of numbers (presented as text).
        encrypted_list = [int(x) for x in encrypted_text] #list of numbers int casted.
    return encrypted_list

def xor_encrypt(normal_text, key):
    """
    function encrypt a string using a given key.
    Args:
        normal_text: a string.
        key: key for encryption.

    Returns:
        function returns the encrypted list.
    """
    # Convert the key to a list of ASCII codes
    key_codes = [ord(c) for c in key]
    # Convert the normal text input to list of ASCII decimal codes.
    Ascii_List = [ord(i) for i in normal_text]
    # Encrypt each byte of the normal text list using the key
    Encrypted_bytes = [byte ^ key_codes[i % len(key_codes)] for i, byte in enumerate(Ascii_List)]
    return Encrypted_bytes

def main():
    file_path = r"C:\Users\JonathanDanzig\Downloads\q\cipher.txt"
    #Converting the text file to a encrypted list.
    encrypted_message = encrypted_textfile_to_list(file_path)
    #Estimating spaces treshold assuming average length of English word is 4.7 chars.
    est_space_th =  round(0.7*(len(encrypted_message)/4.7-1))
    #Collecting and printing the decrypted result.
    L = guess_key_space_filter(encrypted_message, key_size=3, filter_result=True, spaces_th=est_space_th)
    print("key found:", L[0][0])
    print("Decrypt Message:", L[0][1])

# Main function
if __name__ == '__main__':
    main()

