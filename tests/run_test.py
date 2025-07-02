from models import Base, engine
from fill_db import load_constellations_from_file


def main():
    # 1. Создаем таблицы в тестовой БД
    Base.metadata.create_all(engine)
    print("Таблицы созданы в test_star_db")

    # 2. Загружаем тестовые данные
    print("\nЗагрузка тестовых данных...")
    result = load_constellations_from_file(
        "constellations_name.txt",
        "constellations_hints.txt"
    )

    # 3. Проверяем результат
    if result:
        print("\nУспешно загружены данные в тестовую БД!")
    else:
        print("\nОшибка при загрузке данных!")


if __name__ == "__main__":
    main()