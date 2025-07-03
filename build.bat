@echo off

REM Переходим в корневую директорию проекта
cd %~dp0\..

REM Удаляем старую директорию dist
rmdir /s /q dist

REM Создаем новый исполняемый файл
pyinstaller --onefile src/main.py