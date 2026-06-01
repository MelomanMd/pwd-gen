# 🔑 pwd-gen (pdw-gen)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![CLI](https://img.shields.io/badge/interface-CLI-orange.svg)]()

A cryptographically secure, fully customizable, and beautifully styled CLI password generator designed for Linux terminal power-users. Features automated clipboard integration, password entropy analysis, and memorable word-based password generation (xkcd-style). Supports `pwd-gen` and the typo-friendly `pdw-gen` commands.

*Читать на русском ниже (Russian version below).*

---

## ⚡ Features | Возможности

- **Cryptographically Secure**: Built on top of Python's `secrets` module, using hardware-based security for maximum random strength.
- **Bilingual & Typo-Friendly**: Installs both `pwd-gen` and `pdw-gen` commands.
- **Rich Terminal Styling**: Beautiful, high-contrast bold green password display, colored entropy scales, and clean alignments.
- **Strength Assessment**: Precise information entropy calculation in bits with instant rating classification (Weak, Medium, Strong, Very Strong).
- **Interactive "Enter to Copy"**: Interactive prompt makes copying to the clipboard as simple as hitting `Enter` inside your terminal!
- **Word-Based Passwords**: Built-in xkcd-style memorable password generator using local system dictionaries (`/usr/share/dict/words`).
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

## 🛠️ Quick Installation | Быстрая установка

Install instantly from GitHub in one command:
```bash
curl -sSL https://raw.githubusercontent.com/MelomanMd/pwd-gen/main/install.sh | bash
```

### Manual Installation | Ручная установка
```bash
# Clone the repository
git clone https://github.com/MelomanMd/pwd-gen.git
cd pwd-gen

# Run the installation script
./install.sh
```

> [!NOTE]
> The installation script places the command under `~/bin`. Ensure `~/bin` is included in your `$PATH` environment variable. If not, add `export PATH="$HOME/bin:$PATH"` to your `~/.bashrc` or `~/.zshrc`.

---

## 📋 Clipboard Dependencies | Работа с буфером обмена

To support clipboard copy functions (`-C`/`--clip` and interactive copying), you need a system clipboard utility installed on your Linux machine.

* **Ubuntu / Debian / Linux Mint / Pop!_OS:**
  ```bash
  sudo apt update
  sudo apt install -y xclip          # For X11 (Most common)
  sudo apt install -y wl-clipboard   # For Wayland systems
  ```
* **Fedora / RedHat:**
  ```bash
  sudo dnf install -y xclip          # For X11
  sudo dnf install -y wl-clipboard   # For Wayland
  ```
* **Arch Linux / Manjaro:**
  ```bash
  sudo pacman -S xclip               # For X11
  sudo pacman -S wl-clipboard        # For Wayland
  ```

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

Криптографически стойкий, настраиваемый генератор паролей для Linux-терминала. Обладает приятным внешним видом, расчетом энтропии сложности паролей и автоматической интеграцией с буфером обмена. Поддерживает запуск командами `pwd-gen` и `pdw-gen`.

## 🛠️ Установка в одно действие

Запустите следующую команду в терминале для автоматической установки:
```bash
curl -sSL https://raw.githubusercontent.com/MelomanMd/pwd-gen/main/install.sh | bash
```

### Ручная установка
```bash
git clone https://github.com/MelomanMd/pwd-gen.git
cd pwd-gen
./install.sh
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
