from models import Constellation
from database import get_session
session = next(get_session())
# from pillow import Image
# import io
import os


def add_constellation(name, rus_name, image_path, hint=None):
    # использую try-except для обработки ошибок добавления
    # здесь image_path это путь к папке images, который будет реализован в следующей функции
    try:
        existing = session.query(Constellation).filter_by(name=name).first()
        if existing:
            print(f"Созвездие '{name}' уже существует в БД. Пропускаем.")
            return False

        with open(image_path, 'rb') as f:
            image_data = f.read()

        constellation = Constellation(
            name=name,
            rus_name=rus_name,
            image=image_data,
            hint=hint
        )

        session.add(constellation)
        session.commit()
        print(f"Созвездие '{name}' успешно добавлено!")
        return True

    except FileNotFoundError:
        session.rollback()
        print(f"Файл изображения '{image_path}' не найден!")
        return False

    except Exception as e:
        session.rollback()
        print(f"Непредвиденная ошибка при добавлении '{name}': {str(e)}")
        return False


def load_constellations_from_file(file_name_path, file_hints_path):
    # file_hints_path = 'constellations_hints.txt' файл с подсказками
    # file_name_path = 'constellations_name.txt' файл с именами созвездий
    try:
        with open(file_hints_path, 'r', encoding='utf-8') as f_hint:
            hints = {
                rus_name.strip(): hint.strip()
                for line in f_hint if ':' in line
                for rus_name, hint in [line.split(':', 1)]
            }
    except FileNotFoundError:
        print(r'ОШИБКА. Файл "constellations_hints.txt" не найден. Требуется проверка целостности файлов!')
        return False

    if os.path.exists(file_name_path):
        succesful_count = 0
        with open(file_name_path, 'r', encoding='utf-8') as f:
            for index, line in enumerate(f):
                line = line.strip()
                if not line or ':' not in line:
                    continue

                russian_name, english_name = line.split(':', 1)
                photo_folder = "images"
                try:
                    image_path = os.path.join(photo_folder, f'{english_name}.jpeg')

                    if not os.path.exists(image_path):
                        print(f"ОШИБКА. Файл с путем'{image_path}' не найден. Требуется проверка целостности файлов!")
                        return False

                    if russian_name not in hints:
                        print(f"Для созвездия '{russian_name}' нет подсказки!")
                        return False

                    add_constellation(english_name, russian_name, image_path, hints[russian_name])
                    succesful_count += 1

                except FileNotFoundError:
                    print(r"ОШИБКА. Папка 'images' не найдена. Требуется проверка целостности файлов!")
                    return False

            print(f'Блок закончил выполнение без ошибок, число добавленных созвездий = {succesful_count}')
            return True
    else:
        print(r"ОШИБКА. Файл 'constellations_name.txt' не найден. Требуется проверка целостности файлов!")
        return False