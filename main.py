import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from prettytable import PrettyTable

from model import create_tables, drop_tables, Publisher, Shop, Book, Stock, Sale

user = os.getenv('USERNAME')
host = os.getenv('PG_HOST', 'localhost')
port = os.getenv('PG_PORT', '5432')
db = os.getenv('DATABASE', 'netology')

DSN = f'postgresql://{user}@{host}:{port}/{db}'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

query = session.query(Publisher)

records = query.all()

publisher_ids = []
publisher_info = []

for publisher in records:
    publisher_ids.append(str(publisher.id))
    publisher_info.append(f'{publisher.id}-{publisher.name}')

publishers_str = ','.join(publisher_info)

publisher_id = input(f'Введите идентификатор издателя [{publishers_str}]:')

if publisher_id in publisher_ids:
    query = session.query(Stock, Sale, Book, Shop).join(Book, Book.id == Stock.id_book)
    query = query.join(Shop, Shop.id == Stock.id_shop)
    query = query.join(Sale, Stock.id == Sale.id_stock).filter(Book.id_publisher == publisher_id)

    records = query.all()

    report = PrettyTable()
    report.field_names = ["название книги", "название магазина", "стоимость покупки", "дата покупки"]

    for stock, sale, book, shop in records:
        report.add_row([book.title, shop.name, sale.price*stock.count, sale.date_sale])

    print(report)
else:
    print('Неверный идентификатор!')

session.close()
