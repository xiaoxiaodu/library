# -*- coding: utf-8 -*-
import sys, os
sys.path.append('./')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")

from book import models as book_models

if __name__ == '__main__':
    f = open('data.txt')
    # 小城三月`萧红`安徽文艺出版社`赵雪敏`2017.11.29`
    for line in f.readlines():
        fields = line.strip().split('`')
        (bookname, author, publisher, username, borrow_date, return_date) = line.strip().split('`')
        book = book_models.Book.objects.create(
            name=bookname,
            author=author,
            publisher=publisher,
            stock=1
        )
        if username:
            book_models.BorrowRecord.objects.create(
                book_id=book.id,
                username=username,
                borrow_date=borrow_date.replace('.', '-')
            )

            # 库存减1
            book.stock = book.stock - 1
            book.save()
