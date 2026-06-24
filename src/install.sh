#!/usr/bin/env bash

# Конфигурация
SCRIPT_NAME="main.py"
ALIAS_CMD="dv"

# 1. Проверка наличия main.py в текущей директории
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "❌ Ошибка: Файл '$SCRIPT_NAME' не найден в текущей папке ($PWD)"
    exit 1
fi

# Получаем абсолютный путь к текущему скрипту (main.py)
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/$SCRIPT_NAME"
echo "���йден скрипт: $SCRIPT_PATH"

# 2. Находим, где лежит python3
PYTHON_BIN=$(which python3)

if [ -z "$PYTHON_BIN" ]; then
    # Пробуем просто python, если python3 не найден
    PYTHON_BIN=$(which python)
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "❌ Ошибка: Не удалось найти интерпретатор python или python3."
    exit 1
fi

echo "���йден Python: $PYTHON_BIN"

# Директория, куда будем класть наш алиас (рядом с python)
INSTALL_DIR=$(dirname "$PYTHON_BIN")

# Проверка прав на запись в эту директорию
if [ ! -w "$INSTALL_DIR" ]; then
    echo "⚠️ Предупреждение: У вас нет прав на запись в $INSTALL_DIR"
    echo "   Обычно это системная папка (например, /usr/bin). Вам понадобится sudo."
    echo ""
    read -p "Хотите попробовать запустить установку с sudo? (y/n): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Установка отменена."
        exit 0
    fi

    # Запускаем всю оставшуюся часть скрипта через sudo
    exec sudo "$0" "$@"
    exit $?
fi

# 3. Создаем файл-обертку (алиас)
TARGET_PATH="$INSTALL_DIR/$ALIAS_CMD"

cat > "$TARGET_PATH" <<EOF
#!/usr/bin/env bash
# Автоматически сгенерированный алиас для $ALIAS_CMD
# Запускает: python $SCRIPT_PATH
exec python "$SCRIPT_PATH" "\$@"
EOF

# Делаем файл исполняемым
chmod +x "$TARGET_PATH"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ УСПЕХ!"
    echo "Команда '$ALIAS_CMD' установлена глобально."
    echo "Она находится здесь: $TARGET_PATH"
    echo ""
    echo "💡 Как проверить:"
    echo "   Просто введите: $ALIAS_CMD"
    echo ""
    echo
