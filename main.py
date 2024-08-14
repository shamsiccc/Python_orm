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
session.commit()

war_and_peace = Book(title="Война и Мир", id_publisher=1)
childhood = Book(title="Детство", id_publisher=1)
borodino = Book(title="Бородино", id_publisher=2)

session.add_all([war_and_peace, childhood, borodino])

little_reader = Shop(name="Маленький Чтец")
house_book = Shop(name="Дом Книга")
#
session.add_all([little_reader, house_book])
session.commit()

stock1 = Stock(id_book=2, id_shop=1, count=12)
stock2 = Stock(id_book=1, id_shop=1, count=8)
stock3 = Stock(id_book=1, id_shop=2, count=10)
stock4 = Stock(id_book=2, id_shop=2, count=11)
stock5 = Stock(id_book=3, id_shop=2, count=7)
#
session.add_all([stock1, stock2, stock3, stock4, stock5])
session.commit()

sale1 = Sale(price=450, date_sale="17-11-2023", id_stock=1, count=3)
sale2 = Sale(price=670, date_sale="01-03-2023", id_stock=2, count=1)
sale3 = Sale(price=630, date_sale="27-12-2023", id_stock=3, count=1)
sale4 = Sale(price=490, date_sale="05-09-2023", id_stock=4, count=2)
sale5 = Sale(price=520, date_sale="29-08-2021", id_stock=5, count=1)

session.add_all([sale1, sale2, sale3, sale4, sale5])
session.commit()

#Выборка магазинов, продающих целевого публициста

def get_shops(publisher_name):
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)

    if publisher_name.isdigit():
        result = query.filter(publisher_name == Publisher.id).all()
    else:
        result = query.filter(publisher_name == Publisher.name).all()

    for title, shop_name, price, date_sale in result:
        print(f'{title: <16} | {shop_name: <16} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}')


if __name__ == '__main__':
    publisher_name = input('Введите ID или имя публициста: ')
    get_shops(publisher_name)