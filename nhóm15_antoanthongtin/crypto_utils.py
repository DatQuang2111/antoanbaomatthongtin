import base64
import string

class CryptoUtils:
    @staticmethod
    def caesar_decrypt(ciphertext, shift):
        """Decrypt Caesar cipher with given shift"""
        try:
            shift = int(shift)
            result = ""
            for char in ciphertext:
                if char.isalpha():
                    # For uppercase letters
                    if char.isupper():
                        decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    # For lowercase letters
                    else:
                        decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                    result += decrypted_char
                else:
                    result += char
            return result
        except ValueError:
            return ""
    
    @staticmethod
    def vigenere_decrypt(ciphertext, key):
        """Decrypt Vigenère cipher with given key"""
        if not key:
            return ""
        
        key = key.upper()
        result = ""
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                key_char = key[key_index % len(key)]
                shift = ord(key_char) - ord('A')
                
                if char.isupper():
                    decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                
                result += decrypted_char
                key_index += 1
            else:
                result += char
        
        return result
    
    @staticmethod
    def simple_base64_decrypt(ciphertext, key):
        """Simple base64 decryption for educational RSA/AES simulation"""
        try:
            decoded = base64.b64decode(ciphertext).decode('utf-8')
            return decoded
        except:
            return ""
    
    @staticmethod
    def check_caesar(ciphertext, attempted_key, correct_key):
        """Check Caesar cipher attempt"""
        try:
            if attempted_key == correct_key:
                decrypted = CryptoUtils.caesar_decrypt(ciphertext, int(correct_key))
                return True, decrypted
            return False, ""
        except:
            return False, ""
    
    @staticmethod
    def check_vigenere(ciphertext, attempted_key, correct_key):
        """Check Vigenère cipher attempt"""
        if attempted_key.upper() == correct_key.upper():
            decrypted = CryptoUtils.vigenere_decrypt(ciphertext, correct_key)
            return True, decrypted
        return False, ""
    
    @staticmethod
    def check_rsa(ciphertext, attempted_key, correct_key):
        """Check RSA cipher attempt (simplified for educational purposes)"""
        if attempted_key.upper() == correct_key.upper():
            # For educational purposes, we'll use base64 decoding
            decrypted = CryptoUtils.simple_base64_decrypt(ciphertext, correct_key)
            return True, decrypted
        return False, ""
    
    @staticmethod
    def check_aes(ciphertext, attempted_key, correct_key):
        """Check AES cipher attempt (simplified for educational purposes)"""
        if attempted_key == correct_key:
            # For educational purposes, we'll use base64 decoding
            decrypted = CryptoUtils.simple_base64_decrypt(ciphertext, correct_key)
            return True, decrypted
        return False, ""
