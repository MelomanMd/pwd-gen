# 🔑 pwd-gen (pdw-gen)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)](https://github.com/MelomanMd/pwd-gen)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/interface-CLI-orange.svg)]()

A cryptographically secure, fully customizable, and beautifully styled CLI password generator designed for **Linux**, **macOS**, and **Windows** power-users. Features automated clipboard integration, password entropy analysis, and memorable word-based password generation (xkcd-style). Supports `pwd-gen` and the typo-friendly `pdw-gen` commands.

*Читать на русском ниже (Russian version below).*

---

## ⚡ Features | Возможности

- **Cross-Platform**: Full native support for **Linux** (Bash/Zsh), **macOS** (Zsh/Bash), and **Windows** (CMD/PowerShell/Windows Terminal).
- **Cryptographically Secure**: Built on top of Python's `secrets` module, using hardware-based security for maximum random strength.
- **Bilingual & Typo-Friendly**: Installs both `pwd-gen` and `pdw-gen` commands.
- **Rich Terminal Styling**: Beautiful, high-contrast bold green password display, colored entropy scales, and clean alignments. Activates colored ANSI support in Windows natively via `ctypes`.
- **Strength Assessment**: Precise information entropy calculation in bits with instant rating classification (Weak, Medium, Strong, Very Strong).
- **Interactive "Enter to Copy"**: Interactive prompt makes copying to the clipboard as simple as hitting `Enter` inside your terminal! Uses macOS's native `pbcopy`, Windows' native `clip` utility, or Linux clipboard tools.
- **Word-Based Passwords**: Built-in xkcd-style memorable password generator using local system dictionaries (`/usr/share/dict/words` on Linux and macOS) and high-quality robust fallback wordlists.
- **Pipeline Safe**: Automatically detects when output is piped or redirected, disabling interactive prompts to prevent script hangs.

---

## 📸 Demo | Демонстрация

```text
🔑 Сгенерированные пароли:
=============================================
  >>>  #s^%08CL_,B-]4.  <<<
=============================================
📊 Оценка сложности (на один пароль):
  - Длина:    16 символов
  - Сложность: 103.4 бит энтропии
  - Рейтинг:   Very Strong (Очень сильный) ★★★★
---------------------------------------------

📋 Нажмите Enter, чтобы скопировать пароль в буфер обмена (или q для выхода): 
✓ Скопировано в буфер обмена!
```

---

## 🛠️ Installation | Установка

You can install `pwd-gen` natively on **macOS, Windows, and Linux** using Python's package manager `pip`!

### 1. Standard Python Installation (macOS, Windows & Linux - Recommended)
Run this command from any terminal:
```bash
pip install git+https://github.com/MelomanMd/pwd-gen.git
```
*This will automatically compile the command for your OS, making `pwd-gen` and `pdw-gen` available globally as system commands.*

### 2. macOS & Linux Automated Shell Installation
Install instantly using our curl shell script:
```bash
curl -sSL https://raw.githubusercontent.com/MelomanMd/pwd-gen/main/install.sh | bash
```

### 3. Manual Installation (macOS & Linux)
```bash
git clone https://github.com/MelomanMd/pwd-gen.git
cd pwd-gen
./install.sh
```

> [!NOTE]
> The shell installation script places the command under `~/bin`. Ensure `~/bin` is included in your `$PATH` environment variable. If not, add `export PATH="$HOME/bin:$PATH"` to your `~/.bashrc` or `~/.zshrc`.

---

## 📋 Clipboard Dependencies | Работа с буфером обмена

* **macOS**: Works out-of-the-box using the built-in system `pbcopy` utility. No external tools needed!
* **Windows**: Works out-of-the-box using the built-in system `clip` utility. No external tools needed!
* **Linux (Wayland / X11)**: Requires a clipboard tool. Install one depending on your distribution:
  * **Ubuntu / Debian / Mint**: `sudo apt install xclip` (X11) or `sudo apt install wl-clipboard` (Wayland)
  * **Fedora / RedHat**: `sudo dnf install xclip` (X11) or `sudo dnf install wl-clipboard` (Wayland)
  * **Arch Linux / Manjaro**: `sudo pacman -S xclip` (X11) or `sudo pacman -S wl-clipboard` (Wayland)

---

## 🚀 Usage & Parameters | Использование и параметры

```bash
pwd-gen [options]
```

| Short | Long | Description | Default |
| :--- | :--- | :--- | :--- |
| `-l` | `--length` | Length of the password | `16` |
| `-n` | `--count` | Number of passwords to generate | `1` |
| `-u` | `--no-upper` | Exclude uppercase letters (A-Z) | `False` |
| `-L` | `--no-lower` | Exclude lowercase letters (a-z) | `False` |
| `-d` | `--no-digits` | Exclude numbers (0-9) | `False` |
| `-s` | `--no-symbols`| Exclude special symbols | `False` |
| `-a` | `--avoid-ambiguous` | Exclude ambiguous characters (like `1, l, I, 0, o, O, 8, B`) | `False` |
| `-c` | `--custom` | Specify a custom character pool | `None` |
| `-m` | `--memorable` | Generate a word-based memorable password (xkcd-style) | `False` |
| `-w` | `--words` | Number of words for memorable password | `4` |
| `-S` | `--separator`| Word separator for memorable password | `-` |
| `-C` | `--clip` | Automatically copy passwords to the clipboard | `False` |
| `-H` | `--hide` | Generate silently and copy to clipboard (does not show in terminal) | `False` |

---

# 🇷🇺 Версия на русском языке

Кроссплатформенный (Linux, macOS и Windows) генератор паролей для терминала. Обладает приятным дизайном, расчетом энтропии сложности паролей и встроенной интеграцией с буфером обмена Windows (`clip`), macOS (`pbcopy`) и Linux.

## 🛠️ Установка

### 1. Через Python Pip (Рекомендуется для Linux, macOS и Windows)
```bash
pip install git+https://github.com/MelomanMd/pwd-gen.git
```
*Эта команда автоматически настроит исполняемые файлы `pwd-gen` и `pdw-gen` в вашей системе.*

### 2. Скрипт быстрой установки для macOS и Linux
```bash
curl -sSL https://raw.githubusercontent.com/MelomanMd/pwd-gen/main/install.sh | bash
```

## 💡 Примеры использования

1. **Базовый запуск** (генерация 1 надежного пароля из 16 символов):
   ```bash
   pwd-gen
   ```
2. **Генерация 5 паролей длиной по 24 символа**:
   ```bash
   pwd-gen -l 24 -n 5
   ```
3. **Легко запоминающийся пароль из 5 случайных слов с разделителем `_`**:
   ```bash
   pwd-gen -m -w 5 -S _
   ```
4. **Безопасная скрытая генерация** (пароль генерируется скрытно и сразу заносится в буфер обмена, удобно в публичных местах):
   ```bash
   pwd-gen --hide
   ```

---

## 📄 License | Лицензия

This project is licensed under the [MIT License](LICENSE).
