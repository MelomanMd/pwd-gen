#!/usr/bin/env python3
"""
pdw-gen / pwd-gen: Cryptographically secure password generator CLI tool with rich aesthetics.
Developed for Linux, macOS, and Windows systems.
"""

import argparse
import math
import secrets
import shutil
import string
import subprocess
import sys

# Windows terminal styling support
if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

# Color constants for terminal styling
CLR_HEADER = "\033[1;36m"    # Bold Cyan
CLR_SUCCESS = "\033[1;32m"   # Bold Green
CLR_WARNING = "\033[1;33m"   # Bold Yellow
CLR_DANGER = "\033[1;31m"    # Bold Red
CLR_INFO = "\033[1;34m"      # Bold Blue
CLR_MUTED = "\033[90m"       # Dark Grey
CLR_RESET = "\033[0m"        # Reset
CLR_BOLD = "\033[1m"         # Bold
CLR_PWD = "\033[1;92m"        # Bold Bright Green (for high-contrast password)

def get_strength_rating(entropy):
    """
    Categorize password strength based on information entropy (bits).
    """
    if entropy < 40:
        return f"{CLR_DANGER}Weak (Слабый) ★☆☆☆{CLR_RESET}", CLR_DANGER
    elif entropy < 60:
        return f"{CLR_WARNING}Medium (Средний) ★★☆☆{CLR_RESET}", CLR_WARNING
    elif entropy < 80:
        return f"{CLR_SUCCESS}Strong (Сильный) ★★★☆{CLR_RESET}", CLR_SUCCESS
    else:
        return f"{CLR_INFO}Very Strong (Очень сильный) ★★★★{CLR_RESET}", CLR_INFO

def copy_to_clipboard(text):
    """
    Copy generated text to the clipboard using system utilities (pbcopy for macOS, clip for Windows, wl-copy/xclip/xsel for Linux).
    Returns True if successful, False otherwise.
    """
    # Try macOS pbcopy
    if sys.platform == "darwin":
        try:
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        except Exception:
            pass

    # Try Windows clip
    if sys.platform == "win32":
        try:
            subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
            return True
        except Exception:
            pass

    # Try wl-copy (Wayland)
    if shutil.which("wl-copy"):
        try:
            subprocess.run(["wl-copy"], input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            pass

    # Try xclip (X11)
    if shutil.which("xclip"):
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            pass

    # Try xsel (X11)
    if shutil.which("xsel"):
        try:
            subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode("utf-8"), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            pass

    return False

def generate_standard_password(length, use_upper, use_lower, use_digits, use_symbols, avoid_ambiguous, custom_set=None):
    """
    Generate a cryptographically secure random password based on specified criteria.
    """
    if custom_set:
        pool = custom_set
        if not pool:
            raise ValueError("Пользовательский набор символов пуст.")
        return "".join(secrets.choice(pool) for _ in range(length)), len(pool)

    # Define pools
    upper_pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_pool = "abcdefghijklmnopqrstuvwxyz"
    digits_pool = "0123456789"
    symbols_pool = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if avoid_ambiguous:
        ambiguous = "l1Io0O8B"
        upper_pool = "".join(c for c in upper_pool if c not in ambiguous)
        lower_pool = "".join(c for c in lower_pool if c not in ambiguous)
        digits_pool = "".join(c for c in digits_pool if c not in ambiguous)
        symbols_pool = "".join(c for c in symbols_pool if c not in ambiguous)

    categories = []
    if use_upper: categories.append(upper_pool)
    if use_lower: categories.append(lower_pool)
    if use_digits: categories.append(digits_pool)
    if use_symbols: categories.append(symbols_pool)

    if not categories:
        raise ValueError("Не выбран ни один набор символов. Включите хотя бы один.")

    full_pool = "".join(categories)
    pool_size = len(full_pool)

    # If the requested length is smaller than the number of selected categories,
    # we just randomly pick from the complete pool.
    if length < len(categories):
        return "".join(secrets.choice(full_pool) for _ in range(length)), pool_size

    # Guarantee at least one character from each selected category
    password_chars = [secrets.choice(cat) for cat in categories]

    # Fill the remaining length from the general pool
    password_chars += [secrets.choice(full_pool) for _ in range(length - len(categories))]

    # Cryptographically shuffle the resulting character list
    rng = secrets.SystemRandom()
    rng.shuffle(password_chars)

    return "".join(password_chars), pool_size

def load_wordlist():
    """
    Load a list of standard clean words from system dictionaries.
    """
    dict_paths = ["/usr/share/dict/words", "/etc/dictionaries-common/words", "/usr/share/dict/american-english"]
    words = []
    for path in dict_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    word = line.strip()
                    # Keep readable, standard lowercase words
                    if word.isalpha() and word.isascii() and 3 <= len(word) <= 8:
                        words.append(word.lower())
            if words:
                break
        except Exception:
            continue

    if not words:
        # Fallback high-quality memorable words
        words = [
            "correct", "horse", "battery", "staple", "apple", "banana", "cherry", "orange",
            "grape", "melon", "lemon", "lime", "peach", "plum", "berry", "sunny", "windy",
            "cloudy", "rainy", "storm", "river", "forest", "mountain", "valley", "ocean",
            "silver", "golden", "shadow", "winter", "summer", "spring", "autumn", "planet",
            "cosmic", "nebula", "galaxy", "rocket", "matrix", "vertex", "vector", "beacon"
        ]
    return list(set(words)) # unique words only

def generate_memorable_password(word_count, separator, wordlist):
    """
    Generate an xkcd-style memorable password using a list of words.
    """
    chosen = [secrets.choice(wordlist) for _ in range(word_count)]
    return separator.join(chosen), len(wordlist)

def main():
    parser = argparse.ArgumentParser(
        description=f"{CLR_HEADER}🚀 pdw-gen / pwd-gen: Высокозащищенный генератор паролей для Linux, macOS и Windows{CLR_RESET}",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # General configuration
    parser.add_argument("-l", "--length", type=int, default=16, help="Длина генерируемого пароля (символов) [по умолчанию: 16]")
    parser.add_argument("-n", "--count", type=int, default=1, help="Количество генерируемых паролей [по умолчанию: 1]")

    # Character sets exclusions/customizations
    parser.add_argument("-u", "--no-upper", action="store_true", help="Исключить заглавные буквы (A-Z)")
    parser.add_argument("-L", "--no-lower", action="store_true", help="Исключить строчные буквы (a-z)")
    parser.add_argument("-d", "--no-digits", action="store_true", help="Исключить цифры (0-9)")
    parser.add_argument("-s", "--no-symbols", action="store_true", help="Исключить специальные символы")
    parser.add_argument("-a", "--avoid-ambiguous", action="store_true", help="Исключить неоднозначные символы (l, 1, I, o, 0, O, 8, B)")
    parser.add_argument("-c", "--custom", type=str, default=None, help="Использовать только указанные в строке пользовательские символы")

    # Memorable passwords options
    parser.add_argument("-m", "--memorable", action="store_true", help="Генерировать запоминающийся пароль из случайных слов (xkcd-style)")
    parser.add_argument("-w", "--words", type=int, default=4, help="Количество слов для запоминающегося пароля [по умолчанию: 4]")
    parser.add_argument("-S", "--separator", type=str, default="-", help="Разделитель слов для запоминающегося пароля [по умолчанию: -]")

    # Clipboard & Output options
    parser.add_argument("-C", "--clip", action="store_true", help="Скопировать сгенерированный пароль в буфер обмена")
    parser.add_argument("-H", "--hide", action="store_true", help="Скрыть вывод пароля в консоль (автоматически включает копирование в буфер)")
    parser.add_argument("-v", "--version", action="version", version="pwd-gen v1.0.0")

    args = parser.parse_args()

    # If --hide is enabled, we must enable clipboard copying
    should_clip = args.clip or args.hide

    try:
        passwords = []
        entropy = 0.0

        if args.memorable:
            wordlist = load_wordlist()
            vocab_size = len(wordlist)
            for _ in range(args.count):
                pwd, _ = generate_memorable_password(args.words, args.separator, wordlist)
                passwords.append(pwd)
            # Entropy for xkcd-style: word_count * log2(vocabulary_size)
            entropy = args.words * math.log2(vocab_size)
        else:
            # Standard password
            use_upper = not args.no_upper
            use_lower = not args.no_lower
            use_digits = not args.no_digits
            use_symbols = not args.no_symbols

            # Create standard passwords
            for _ in range(args.count):
                pwd, pool_size = generate_standard_password(
                    args.length, use_upper, use_lower, use_digits, use_symbols, 
                    args.avoid_ambiguous, args.custom
                )
                passwords.append(pwd)
            # Entropy: length * log2(pool_size)
            if passwords:
                entropy = len(passwords[0]) * math.log2(pool_size)

        # Handle clipboard copy
        clip_msg = ""
        if should_clip:
            joined_passwords = "\n".join(passwords)
            success = copy_to_clipboard(joined_passwords)
            if success:
                clip_msg = f"{CLR_SUCCESS}✓ Скопировано в буфер обмена!{CLR_RESET}"
            else:
                clip_msg = f"{CLR_DANGER}⚠ Ошибка: Не удалось скопировать (буфер обмена не найден или недоступен){CLR_RESET}"

        # Visual formatting
        rating_str, rating_color = get_strength_rating(entropy)

        if args.hide:
            # Hidden mode
            print(f"\n{CLR_HEADER}🔑 pdw-gen (Скрытый режим){CLR_RESET}")
            print("=" * 45)
            print(f" Количество паролей:  {CLR_BOLD}{args.count}{CLR_RESET}")
            print(f" Надежность пароля:  {rating_str} ({entropy:.1f} бит)")
            print("-" * 45)
            if clip_msg:
                print(clip_msg)
            print("=" * 45 + "\n")
        else:
            # Normal verbose mode
            print(f"\n{CLR_HEADER}🔑 Сгенерированные пароли:{CLR_RESET}")
            print("=" * 45)
            if len(passwords) == 1:
                print(f"  >>>  {CLR_PWD}{passwords[0]}{CLR_RESET}  <<<")
            else:
                for idx, pwd in enumerate(passwords, 1):
                    print(f"  {idx:2d}. {CLR_PWD}{pwd}{CLR_RESET}")
            print("=" * 45)

            print(f"{CLR_MUTED}📊 Оценка сложности (на один пароль):{CLR_RESET}")
            if args.memorable:
                print(f"  - Тип:      Легко запоминающийся (Слова: {args.words}, разделитель: '{args.separator}')")
            else:
                print(f"  - Длина:    {args.length} символов")
            print(f"  - Сложность: {entropy:.1f} бит энтропии")
            print(f"  - Рейтинг:   {rating_str}")
            print("-" * 45)
            if clip_msg:
                print(clip_msg)
                print("-" * 45)
            print()

            # Interactive prompt to copy to clipboard if stdin and stdout are interactive TTYs
            # and the password hasn't already been copied via --clip / --hide flags.
            if sys.stdout.isatty() and sys.stdin.isatty() and not should_clip:
                if len(passwords) == 1:
                    try:
                        user_input = input(f"📋 Нажмите {CLR_BOLD}Enter{CLR_RESET}, чтобы скопировать пароль в буфер обмена (или {CLR_BOLD}q{CLR_RESET} для выхода): ").strip().lower()
                        if user_input != 'q':
                            success = copy_to_clipboard(passwords[0])
                            if success:
                                print(f"{CLR_SUCCESS}✓ Скопировано в буфер обмена!{CLR_RESET}\n")
                            else:
                                print(f"{CLR_DANGER}⚠ Ошибка: Не удалось скопировать (буфер обмена не найден или недоступен){CLR_RESET}\n")
                    except (KeyboardInterrupt, EOFError):
                        print()
                else:
                    try:
                        user_input = input(f"📋 Нажмите {CLR_BOLD}Enter{CLR_RESET}, чтобы скопировать все пароли, или введите номер {CLR_BOLD}(1-{len(passwords)}){CLR_RESET} для копирования (или {CLR_BOLD}q{CLR_RESET} для выхода): ").strip().lower()
                        if user_input != 'q':
                            if not user_input:
                                success = copy_to_clipboard("\n".join(passwords))
                                if success:
                                    print(f"{CLR_SUCCESS}✓ Все {len(passwords)} паролей скопированы в буфер обмена!{CLR_RESET}\n")
                                else:
                                    print(f"{CLR_DANGER}⚠ Ошибка: Не удалось скопировать (буфер обмена не найден или недоступен){CLR_RESET}\n")
                            elif user_input.isdigit():
                                idx = int(user_input) - 1
                                if 0 <= idx < len(passwords):
                                    success = copy_to_clipboard(passwords[idx])
                                    if success:
                                        print(f"{CLR_SUCCESS}✓ Пароль #{idx+1} скопирован в буфер обмена!{CLR_RESET}\n")
                                    else:
                                        print(f"{CLR_DANGER}⚠ Ошибка: Не удалось скопировать (буфер обмена не найден или недоступен){CLR_RESET}\n")
                                else:
                                    print(f"{CLR_DANGER}⚠ Неверный номер пароля.{CLR_RESET}\n")
                    except (KeyboardInterrupt, EOFError):
                        print()

    except Exception as e:
        print(f"\n{CLR_DANGER}❌ Ошибка: {str(e)}{CLR_RESET}\n", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
