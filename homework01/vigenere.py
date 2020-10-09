def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    for index, char in enumerate(plaintext):
        key = ord(keyword[index % len(keyword)].lower())
        if 'A' <= char <= 'Z':
            ciphertext += chr((ord(char) - ord("A") + key - ord("a")) % 26 + ord("A"))
        elif 'a' <= char <= 'z':
            ciphertext += chr((ord(char) - ord("a") + key - ord("a")) % 26 + ord("a"))
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    for index, char in enumerate(ciphertext):
        key = ord(keyword[index % len(keyword)].lower())
        if 'A' <= char <= 'Z':
            plaintext += chr((ord(char) - ord("A") - key + ord("a")) % 26 + ord("A"))
        elif 'a' <= char <= 'z':
            plaintext += chr((ord(char) - ord("a") - key + ord("a")) % 26 + ord("a"))
        else:
            plaintext += char
    return plaintext
