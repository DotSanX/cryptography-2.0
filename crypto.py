import getpass
from cryptography.fernet import Fernet
import json
import os
import logging

PASSWORD_FILE = 'password.json'
KEY_FILE = 'key.key'
LOG_FILE = 'log.log'

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as file:
        file.write(key)
    logging.info('Key generated')
    return key

def load_key():
    """ Загружаеам ключ шифрования из файла """
    return open(KEY_FILE, "rb").read()

def encrypt_data(data, key):
    """ Шифрует данные с использованием ключа """
    encrypted_data = Fernet(key).encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data, key):
    """ Расшифровывает данные с использованием ключа """
    decrypted_data = Fernet(key).decrypt(encrypted_data)
    return decrypted_data.decode()

def is_password_strong(password):
    """ Функция для проверки сложности пароля"""
    if len(password) < 5:
        return False
    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    return has_digit and has_upper and has_lower

def get_password(prompt, show_password):
    """ Получение пароля от пользователя с возможность отображения ввода """
    if show_password == "Да":
        return input(prompt)
    return getpass.getpass(prompt)
    
    

def create_and_store_password():
    """ Создает и сохраняет пароль в файл JSON """
    if os.path.exists(PASSWORD_FILE) and os.path.exists(KEY_FILE):
        logging.warning(' Попытка создания нового пароля, когда зашифрованный файл уже существует')
        return
    key = generate_key()
    while True:
        # Создание и сохранение пароля
        show_password = input("Хотите ли Вы видеть введённый пароль (да/нет): ").lower() == 'да'
        created_password = get_password("Создайте пароль: ", show_password)
        confirm_password = get_password("Повторите пароль: ", show_password)
        if created_password != confirm_password:
            logging.warning(' Пароли не совпадают при попытке создания')
            print("Пароли не совпадают. Попробуйте еще раз.")

        if is_password_strong(created_password):
            logging.info(' Пароль создан')
            encrypted_password = encrypt_data(created_password, key)
            password = {"password": encrypted_password.decode()}
            with open(PASSWORD_FILE, 'w') as file:
                json.dump(password, file)
            logging.info('Пароль успешно создан и сохранен')
            print("Пароль успешно создан и сохранен")
            break
        else:
            logging.warning(' Пароль слишком простой. Попробуйте еще раз.')
            print("Пароль слишком простой. Попробуйте еще раз.")

def user_interface():
    """ Интерфейс пользователя для работы с менеджером паролей """
    print(" Добро пожаловать в менеджер паролей!")
    if not os.path.exists(PASSWORD_FILE) or not os.path.exists(KEY_FILE):
        print(" Зашифрованный пароль или ключ не найден. Сначала создайте пароль ")
        create_and_store_password()
    key = load_key()
    with open(PASSWORD_FILE, 'r') as file:
        password_data = json.load(file)
        created_password = decrypt_data(password_data['password'], key)
        print(f" Зашифрованный пароль: {created_password}") 

#Аутентификация пользователя

while True:
    show_password = input(" Хотите ли Вы видеть вводимый пароль? [да/нет]").lower() == 'да'
    entered_password = get_password(f"Введите ваш пароль для доступа: ", show_password)
    if entered_password == created_password:
        break
    else:
        logging.warning('Пользователь ввел неверный пароль')
        print("Неверный пароль. Попробуйте еще раз.")


key = generate_key()

while True:
    print(" Выберите действие:")
    choice = input(" 1. Зашифровать файл\n 2. Расшифровать файл\n 3. Выход\n")
    if choice == '1':
        data_to_encrypt = input(" Введите данные для шифрования: ")
        encrypted_data = encrypt_data(data_to_encrypt, key)
        print(f" Зашифрованный файл: {encrypted_data}")
    elif choice == '2':
        encrypted_data = input(" Введите зашифрованный файл: ")
        decrypted_data = decrypt_data(encrypted_data, key)
        print(f" Расшифрованный файл: {decrypted_data}")
    elif choice == '3':
        break





            

