@echo on

REM Переходим в корневую директорию проекта
cd %~dp0\..

REM Проверяем текущую рабочую директорию
echo Current working directory: %cd%

REM переходим к данному проекту constellation_learning_program
cd constellation_learning_program

REM проверяем текущую рабочую директорию
echo Current working directory: %cd%

REM Удаляем старую директорию dist
if exist dist (
    echo Removing old dist directory...
    rmdir /s /q dist
) else (
    echo No old dist directory found.
)

REM Удаляем кэш pyinstaller
if exist build (
    echo Removing old build directory...
    rmdir /s /q build
) else (
    echo No old build directory found.
)

REM Проверяем версию Python
echo Checking Python version...
python --version

REM Определяем абсолютный путь к файлу main.py
set MAIN_PY=%cd%\src\main.py

REM Проверяем существование файла main.py
if exist "%MAIN_PY%" (
    echo File main.py exists at: %MAIN_PY%
) else (
    echo File main.py does not exist at: %MAIN_PY%
    pause
    exit /b 1
)

REM Создаем новый исполняемый файл
echo Running PyInstaller...
pyinstaller --onefile ^
            --add-data "src/constellations_name.txt;src" ^
            --add-data "src/constellations_hints.txt;src" ^
            --add-data "src/images;images" ^
            src/main.py

REM Проверяем, что файл создан
if exist dist\main.exe (
    echo Executable file created successfully.
    echo Path to executable: %MAIN_PY%
    for %%i in (dist\main.exe) do (
        echo File created at: %%~ti
    )
) else (
    echo Failed to create executable file.
)

REM Проверяем содержимое директории dist
echo Contents of dist directory:
dir dist

REM Задерживаем закрытие консоли
pause