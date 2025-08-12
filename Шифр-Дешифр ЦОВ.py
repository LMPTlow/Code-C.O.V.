# Определяем раскладку клавиатуры по строкам
COW_KEYBOARD = {
    'А': ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ'],
    'Б': ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э'],
    'В': ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', 'ё']  # В9 = ё
}

# Русский алфавит для шифрования цифр (заглавные буквы)
RUS_ALPHABET = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И',
    'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
    'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь',
    'Э', 'Ю', 'Я'
]

# Создаем обратный словарь для быстрого поиска
LETTER_TO_CODE = {}
for row, letters in COW_KEYBOARD.items():
    for index, letter in enumerate(letters):
        LETTER_TO_CODE[letter] = (row, index)
        LETTER_TO_CODE[letter.upper()] = (row, index)

def number_to_cow(number):
    """Конвертирует число в буквенный код по правилам ЦОВ"""
    if 1 <= number <= 33:
        return RUS_ALPHABET[number - 1]
    else:
        digits = list(str(number))
        result = []
        for d in digits:
            num = int(d)
            if num == 0:
                result.append(RUS_ALPHABET[9])  # 0 → И
            else:
                result.append(RUS_ALPHABET[num - 1])
        return ''.join(result)

def cow_to_number(cow_str):
    """Конвертирует буквенный код числа обратно в цифры"""
    result = 0
    for char in cow_str:
        if char in RUS_ALPHABET:
            num = RUS_ALPHABET.index(char) + 1
            if num == 10:  # И → 0
                num = 0
            result = result * 10 + num
    return result if result != 0 else 33  # Я → 33

def encrypt_cow(text):
    """Шифрует текст в код ЦОВ"""
    encrypted_parts = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # Обработка цифр
        if char.isdigit():
            num_str = char
            while i + 1 < len(text) and text[i+1].isdigit():
                i += 1
                num_str += text[i]
            encrypted_parts.append(number_to_cow(int(num_str)))
            i += 1
            continue
            
        if char == ' ':
            encrypted_parts.append('(_)')
        elif char in LETTER_TO_CODE:
            row, index = LETTER_TO_CODE[char]
            prefix = '!' if char.isupper() else ''
            encrypted_parts.append(f"{prefix}{row}{index}")
        else:
            encrypted_parts.append(char)
        i += 1
    return ' '.join(encrypted_parts)

def decrypt_cow(code):
    """Расшифровывает код ЦОВ обратно в текст"""
    decrypted_parts = []
    i = 0
    while i < len(code):
        if code[i] == ' ':
            i += 1
            continue
            
        # Обработка кодов ЦОВ (!А10, Б3 и т.д.)
        if code[i] in {'А', 'Б', 'В', '!'}:
            original_i = i
            is_upper = False
            
            if code[i] == '!':
                is_upper = True
                i += 1
                if i >= len(code):
                    decrypted_parts.append('?!')
                    break
            
            if i < len(code) and code[i] in {'А', 'Б', 'В'}:
                row = code[i]
                i += 1
                num_str = ''
                while i < len(code) and code[i].isdigit():
                    num_str += code[i]
                    i += 1
                
                if num_str:
                    try:
                        num = int(num_str)
                        letters = COW_KEYBOARD[row]
                        effective_index = num % len(letters)
                        if row == 'В' and num == 9:
                            letter = 'ё'
                        else:
                            letter = letters[effective_index]
                        decrypted_parts.append(letter.upper() if is_upper else letter)
                        continue
                    except:
                        pass
            
            # Если не получилось как код ЦОВ, возвращаемся
            i = original_i
        
        # Обработка цифр (одиночные заглавные русские буквы)
        if code[i] in RUS_ALPHABET:
            # Проверяем, что это действительно одиночная буква-цифра
            if (i + 1 >= len(code)) or (code[i+1] not in RUS_ALPHABET):
                if (i == 0) or (code[i-1] not in {'А', 'Б', 'В', '!'}):
                    decrypted_parts.append(str(cow_to_number(code[i])))
                    i += 1
                    continue
        
        # Обработка пробела
        if code.startswith('(_)', i):
            decrypted_parts.append(' ')
            i += 4
            continue
            
        # Если ничего не подошло - оставляем как есть
        decrypted_parts.append(code[i])
        i += 1
            
    return ''.join(decrypted_parts)

def main():
    print("Добро пожаловать в переводчик шифра ЦОВ!")
    print("Made by LMPT")
    print("License AEL© - Atlas Entertainment License 1.0.0")
    
    while True:
        print("\nВыберите действие:")
        print("1. Зашифровать текст")
        print("2. Расшифровать код")
        print("3. Выход")
        choice = input("Ваш выбор (1/2/3): ").strip()
        
        if choice == '1':
            text = input("Введите текст для шифрования: ")
            encrypted = encrypt_cow(text)
            print(f"Результат: {encrypted}")
        elif choice == '2':
            code = input("Введите код для расшифровки: ")
            decrypted = decrypt_cow(code)
            print(f"Результат: {decrypted}")
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()