from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Numeric
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = 'publisher'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)

    books: Mapped[List['Book']] = relationship(back_populates='publisher', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'Publisher(id={self.id!r}, name={self.name!r}'


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"))

    publisher: Mapped['Publisher'] = relationship(back_populates='books')
    stock: Mapped['Stock'] = relationship(back_populates='books')

    def __repr__(self) -> str:
        return f'Book(id={self.id!r}, title={self.title!r})'


class Stock(Base):
    __tablename__ = 'stock'

    id: Mapped[int] = mapped_column(primary_key=True)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id"))
    id_shop: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    count: Mapped[int] = mapped_column(BigInteger(), nullable=False)

    book: Mapped['Book'] = relationship(back_populates='stock')
    shop: Mapped['Shop'] = relationship(back_populates='stock')
    sale: Mapped['Sale'] = relationship(back_populates='stock')

    def __repr__(self) -> str:
        return f'Stock(id={self.id!r}, book_id={self.id_book!r}, shop_id={self.id_shop!r},' \
               f'count={self.count!r}'


class Shop(Base):
    __tablename__ = 'shop'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)

    books: Mapped[List['Book']] = relationship(back_populates='shop', cascade='all, delete-orphan')
    stock: Mapped[List['Stock']] = relationship(back_populates='shop')

    def __repr__(self) -> str:
        return f'Shop(id={self.id!r}, name={self.name!r}'


class Sale(Base):
    __tablename__ = 'sale'

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    data_sale: Mapped[str] = mapped_column(DateTime(), nullable=False)
    id_stock: Mapped[int] = mapped_column(ForeignKey("stock.id"))
    count: Mapped[int] = mapped_column(BigInteger(), nullable=False)

    stock: Mapped['Stock'] = relationship(back_populates='sales')

    def __repr__(self) -> str:
        return f'Sale(id={self.id!r}, price={self.price!r}, date_sale={self.data_sale!r}, count={self.count!r}'

