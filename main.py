import os
import base64
import hashlib
import hmac
import secrets
import string

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def encrypt_password(password):
    key = os.urandom(32)
    cipher_text = base64.b64encode(hmac.new(key, password.encode(), hashlib.sha256).digest())
    return key + cipher_text

def decrypt_password(encrypted_password):
    key = encrypted_password[:32]
    cipher_text = encrypted_password[32:]
    return hmac.new(key, base64.b64decode(cipher_text), hashlib.sha256).digest().decode()

def save_passwords(passwords):
    with open('passwords.txt', 'wb') as f:
        for site, password in passwords.items():
            encrypted_password = encrypt_password(password)
            f.write(f'{site}:{encrypted_password}\n'.encode())

def load_passwords():
    passwords = {}
    with open('passwords.txt', 'rb') as f:
        for line in f:
            site, encrypted_password = line.decode().split(':')
            passwords[site] = decrypt_password(encrypted_password)
    return passwords

def main():
    passwords = {}
    while True:
        print('1. Yangi parol yaratish')
        print('2. Parollar ro\'yxatini ko\'rish')
        print('3. Chiqish')
        choice = input('Izoh: ')
        if choice == '1':
            site = input('Sayt nomi: ')
            password_length = int(input('Parol uzunligi: '))
            password = generate_password(password_length)
            passwords[site] = password
            save_passwords(passwords)
            print(f'Parol: {password}')
        elif choice == '2':
            passwords = load_passwords()
            for site, password in passwords.items():
                print(f'{site}: {password}')
        elif choice == '3':
            break
        else:
            print('Izoh: Xato tanlov')

if __name__ == '__main__':
    main()
