#!/usr/bin/env bash
# Automated installation script for pdw-gen / pwd-gen
#
# Usage (Local): ./install.sh
# Usage (Remote): curl -sSL https://raw.githubusercontent.com/MelomanMd/pwd-gen/main/install.sh | bash

set -e

# Formatting colors
CLR_GREEN="\033[1;32m"
CLR_YELLOW="\033[1;33m"
CLR_CYAN="\033[1;36m"
CLR_RED="\033[1;31m"
CLR_RESET="\033[0m"
CLR_BOLD="\033[1m"

echo -e "${CLR_CYAN}====================================================${CLR_RESET}"
echo -e "${CLR_CYAN}🚀 Installing pdw-gen / pwd-gen | Установка pwd-gen${CLR_RESET}"
echo -e "${CLR_CYAN}====================================================${CLR_RESET}"

BIN_DIR="$HOME/bin"
mkdir -p "$BIN_DIR"

# Determine installation source (local directory or remote download)
if [ -f "pdw-gen" ]; then
    echo -e "${CLR_GREEN}[1/3]${CLR_RESET} Copying script locally... | Копирование локального скрипта..."
    cp pdw-gen "$BIN_DIR/pdw-gen"
else
    echo -e "${CLR_GREEN}[1/3]${CLR_RESET} Downloading script from GitHub... | Скачивание скрипта с GitHub..."
    curl -sSL "https://raw.githubusercontent.com/MelomanMd/pwd-gen/main/pdw-gen" -o "$BIN_DIR/pdw-gen"
fi

# Set executable permissions
echo -e "${CLR_GREEN}[2/3]${CLR_RESET} Setting executable permissions... | Настройка прав на исполнение..."
chmod +x "$BIN_DIR/pdw-gen"

# Create/Update symbolic link
echo -e "${CLR_GREEN}[3/3]${CLR_RESET} Creating symlink pwd-gen... | Создание символической ссылки..."
ln -sf "$BIN_DIR/pdw-gen" "$BIN_DIR/pwd-gen"

echo -e "${CLR_CYAN}----------------------------------------------------${CLR_RESET}"

# Verify if BIN_DIR is in user's PATH environment variable
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${CLR_YELLOW}⚠️  WARNING: $BIN_DIR is not in your \$PATH.${CLR_RESET}"
    echo -e "${CLR_YELLOW}⚠️  ВНИМАНИЕ: Путь $BIN_DIR отсутствует в вашей переменной \$PATH.${CLR_RESET}"
    echo -e ""
    echo -e "To run the command from anywhere, add the following line to your ~/.bashrc or ~/.zshrc:"
    echo -e "Чтобы запускать команду из любого места, добавьте эту строку в ваш ~/.bashrc или ~/.zshrc:"
    echo -e "  ${CLR_BOLD}export PATH=\"\$HOME/bin:\$PATH\"${CLR_RESET}"
    echo -e "And reload your terminal. | И перезапустите терминал."
else
    echo -e "${CLR_GREEN}✨ Installation successful! | Установка завершена успешно!${CLR_RESET}"
    echo -e "You can now run '${CLR_BOLD}pwd-gen${CLR_RESET}' or '${CLR_BOLD}pdw-gen${CLR_RESET}' from any terminal window."
    echo -e "Вы можете запускать '${CLR_BOLD}pwd-gen${CLR_RESET}' или '${CLR_BOLD}pdw-gen${CLR_RESET}' из любого терминала."
fi
echo -e "${CLR_CYAN}====================================================${CLR_RESET}"
