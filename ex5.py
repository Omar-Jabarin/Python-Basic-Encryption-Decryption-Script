import os
import json

LETTERS_NUM = ord('z')-ord('a')+1
def aux_char_cycle(c: str, n: int):
    assert (len(c) == 1)
    if c.isupper():
        return chr(ord('A') + ((ord(c) - ord('A') + n) % LETTERS_NUM))
    if c.islower():
        return chr(ord('a') + ((ord(c) - ord('a') + n) % LETTERS_NUM))
    return c
class Cipher:
    def encrypt(self, msg: str) -> str:
        pass

    def decrypt(self, msg: str) -> str:
        pass


class CaesarCipher(Cipher):
    def __init__(self, key: int):
        self.key = key

    def encrypt(self, msg: str) -> str:
        rv = ""
        for c in msg:
            if c.isalpha():
                rv += aux_char_cycle(c, self.key)
            else:
                rv += c
        return rv

    def decrypt(self, msg: str) -> str:
        return CaesarCipher(-self.key).encrypt(msg)


class VigenereCipher(Cipher):
    def __init__(self, key: list):
        self.key = key

    def encrypt(self, msg: str) -> str:
        idx = 0
        rv = ""
        for c in msg:
            rv += aux_char_cycle(c, self.key[idx])
            if c.isalpha():
                idx = (idx + 1) % len(self.key)
        return rv

    def decrypt(self, msg: str) -> str:
        return VigenereCipher([-x % LETTERS_NUM for x in self.key]).encrypt(msg)


def getVigenereFromStr(key: str) -> VigenereCipher:
    my_list = []
    for c in key:
        if c.isupper():
            my_list.append(ord(c) - ord("A"))
        if c.islower():
            my_list.append(ord(c) - ord("a"))
    return VigenereCipher(my_list)


def auxEncryptionSystem(cipher: Cipher, dir_path: str, encrypt_mode: bool):
    files_list = os.listdir(dir_path)
    txt_files_list = [file for file in files_list if file.endswith(".txt")]
    enc_files_list = [file for file in files_list if file.endswith(".enc")]
    if encrypt_mode:
        for filename in txt_files_list:
            filepath = os.path.join(dir_path, filename)
            with open(filepath, "r") as curr_file:
                curr_file_content = curr_file.read()

            enc_content = cipher.encrypt(curr_file_content)
            base_filename, filename_ext = os.path.splitext(filename)
            enc_filename = base_filename + ".enc"
            filepath = os.path.join(dir_path, enc_filename)
            with open(filepath, "w") as enc_file:
                enc_file.write(enc_content)

    else:
        for filename in enc_files_list:
            filepath = os.path.join(dir_path, filename)
            with open(filepath, "r") as curr_file:
                curr_file_content = curr_file.read()

            dec_content = cipher.decrypt(curr_file_content)
            base_filename, filename_ext = os.path.splitext(filename)
            dec_filename = base_filename + ".txt"
            filepath = os.path.join(dir_path, dec_filename)
            with open(filepath, "w") as dec_file:
                dec_file.write(dec_content)


def loadEncryptionSystem(dir_path: str):
    config_path = os.path.join(dir_path, "config.json")
    with open(config_path, "r") as f:
        data = json.load(f)
        mode = (data['encrypt'] == "True")
        if data['type'] == "Caesar":
            auxEncryptionSystem(CaesarCipher(int(data['key'])), dir_path, mode)
        if data['type'] == "Vigenere":
            if type(data['key']) is str:
                auxEncryptionSystem(getVigenereFromStr(data['key']), dir_path, mode)

            elif type(data['key']) is list:
                auxEncryptionSystem(VigenereCipher(data['key']), dir_path, mode)
