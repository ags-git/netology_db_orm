import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    # homeworks = relationship("Homework", back_populates="course")


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref="sales")


def drop_tables(engine):
    Base.metadata.drop_all(engine)

def create_tables(engine):
    Base.metadata.create_all(engine)


# DSN = "postgresql://postgres:postgres@localhost:5432/netology_db"
# engine = sqlalchemy.create_engine(DSN)
# create_tables(engine)
#
# # сессия
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # создание объектов
# js = Course(name="JavaScript")
# print(js.id)
# hw1 = Homework(number=1, description="первое задание", course=js)
# hw2 = Homework(number=2, description="второе задание (сложное)", course=js)
#
# session.add(js)
# print(js.id)
# session.add_all([hw1, hw2])
# session.commit()  # фиксируем изменения
# print(js.id)
#
#
# # запросы
# q = session.query(Course).join(Homework.course).filter(Homework.number == 1)
# print(q)
# for s in q.all():
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)
#
# # вложенный запрос
# subq = session.query(Homework).filter(Homework.description.like("%сложн%")).subquery("simple_hw")
# q = session.query(Course).join(subq, Course.id == subq.c.course_id)
# print(q)
# for s in q.all():
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)
#
#
# # обновление объектов
# session.query(Course).filter(Course.name == "JavaScript").update({"name": "NEW JavaScript"})
# session.commit()  # фиксируем изменения
#
#
# # удаление объектов
# session.query(Homework).filter(Homework.number > 1).delete()
# session.commit()  # фиксируем изменения
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
