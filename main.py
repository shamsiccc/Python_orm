import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = "postgresql://postgres:QwerAE86@localhost:5432/netology_db"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Создание объектов
tolstoi = Publisher(name="Толстой")
lermontov = Publisher(name="Лермонтов")

session.add_all([tolstoi, lermontov])

war_and_peace = Book(title="Война и Мир", id_publisher=tolstoi)
childhood = Book(title="Детство", id_publisher=tolstoi)
borodino = Book(title="Бородино", id_publisher=lermontov)

session.add_all([war_and_peace, childhood, borodino])

little_reader = Shop(name="Маленький Чтец")
house_book = Shop(name="Дом Книга")

session.add_all([little_reader, house_book])

stock1 = Stock(id_book=childhood, id_shop=little_reader, count=12)
stock2 = Stock(id_book=war_and_peace, id_shop=little_reader, count=8)
stock3 = Stock(id_book=war_and_peace, id_shop=house_book, count=10)
stock4 = Stock(id_book=childhood, id_shop=house_book, count=11)
stock5 = Stock(id_book=borodino, id_shop=house_book, count=7)

session.add_all([stock1, stock2, stock3, stock4, stock5])

sale1 = Sale(price=450, date_sale="17-11-2023", id_stock=stock1, count=3)
sale2 = Sale(price=670, date_sale="01-03-2023", id_stock=stock2, count=1)
sale3 = Sale(price=630, date_sale="27-12-2023", id_stock=stock3, count=1)
sale4 = Sale(price=490, date_sale="05-09-2023", id_stock=stock4, count=2)
sale5 = Sale(price=520, date_sale="29-08-2021", id_stock=stock5, count=1)

session.add_all([sale1, sale2, sale3, sale4, sale5])
session.commit()

# Выборка магазинов, продающих целевого издателя
publisher_name = input("Введите имя издателя: ")
publishers = session.query(Publisher).filter(Publisher.name.ilike(f"%{publisher_name}%")).all()
if not publishers:
    print("Издатель не найден")
else:
    for publisher in publishers:
        sales_data = (session.query(
            Book.title,
            Shop.name,
            Sale.price,
            Sale.date_sale
        ).select_from(Book)
        .join(Stock)
        .join(Shop)
        .join(Sale)
        .filter(Book.id_publisher == publisher.id).all())

        if not sales_data:
            print("Нет данных о покупке данного издателя.")
        else:
            print("Название книги | Название магазина | Стоимость покупки | Дата покупки ")
            for title, shop_name, price, date in sales_data:
                print(f"{title}, {shop_name}, {price}, {date}")

session.close()
