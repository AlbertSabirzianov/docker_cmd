@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ==========================================
echo   УСТАНОВЩИК КОМАНДЫ 'dv' ДЛЯ WINDOWS
echo ==========================================
echo.

REM 1. Проверка наличия main.py
if not exist "main.py" (
    echo [ОШИБКА] Файл 'main.py' не найден в текущей папке!
    echo Положите main.py туда же, где лежит этот скрипт install_dv.bat
    pause
    exit /b 1
)

REM Получаем абсолютный путь к main.py (чтобы он работал даже если мы скопируем скрипт в другое место)
set "MAIN_PY_PATH=%~dp0main.py"

echo [INFO] Найден main.py: %MAIN_PY_PATH%
echo.

REM 2. Поиск пути к python.exe
echo [INFO] Ищем python.exe...
for /f "delims=" %%i in ('where python 2^>nul') do set "PYTHON_EXE=%%i"

if "%PYTHON_EXE%"=="" (
    echo [ОШИБКА] Не удалось найти python.exe.
    echo Убедитесь, что Python установлен и добавлен в PATH.
    pause
    exit /b 1
)

echo [SUCCESS] Найден Python: %PYTHON_EXE%

REM Извлекаем только путь к папке (без имени файла python.exe)
for %%i in ("%PYTHON_EXE%") do set "PYTHON_DIR=%%~dpi"
echo [INFO] Папка установки Python: %PYTHON_DIR%
echo.

REM 3. Создание временного файла dv.bat с жестким путем к main.py
echo [INFO] Создаем файл-обертку dv.bat...
(
    echo @echo off
    echo python "%MAIN_PY_PATH%" %%*
) > "%TEMP%\dv_install.bat"

REM 4. Копирование в папку Python (требуются права админа)
echo [INFO] Копируем dv.bat в %PYTHON_DIR% ...
copy /Y "%TEMP%\dv_install.bat" "%PYTHON_DIR%dv.bat" >nul

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo   ✅ УСПЕХ!
    echo   Команда 'dv' теперь доступна везде.
    echo ==========================================
    echo.
    echo Как проверить:
    echo   1. Откройте НОВУЮ консоль (cmd или PowerShell).
    echo   2. Введите: dv --help (или просто dv)
    echo   3. Скрипт запустит ваш main.py.
    echo.
) else (
    echo.
    echo ==========================================
    echo   ❌ ОШИБКА! Не удалось скопировать файл.
    echo   Скорее всего, у вас нет прав администратора.
    echo   Пожалуйста, запустите install_dv.bat ОТ ИМЕНИ АДМИНИСТРАТОРА.
    echo ==========================================
)

del "%TEMP%\dv_install.bat" >nul
endlocal
pause
