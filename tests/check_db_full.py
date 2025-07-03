from src.models import Constellation
from src.database import get_session
session = next(get_session())


def check_constellations():
    # вывожу первые 5 созвездий из ЗАПОЛНЕННОЙ бд
    constellations = session.query(Constellation).limit(5).all()
    print("Последние добавленные созвездия:")
    for c in constellations:
        print(f"\nID: {c.id}")
        print(f"Английское название: {c.name}")
        print(f"Русское название: {c.rus_name}")
        print(f"Размер изображения: {len(c.image)} байт")
        print(f"Подсказка: {c.hint[:50]}...")
    # Проверяю общее число созвездий. В моей работе их должно быть 87
    count = session.query(Constellation).count()
    print(f"\nВсего созвездий в БД: {count}")


if __name__ == "__main__":
    check_constellations()