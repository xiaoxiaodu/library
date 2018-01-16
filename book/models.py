# -*- coding: utf-8 -*-

from django.db import models


class Book(models.Model):
    """
    图书
    """
    name = models.CharField(max_length=128)  # 书名
    author = models.CharField(max_length=64, default='')  # 作者
    publisher = models.CharField(max_length=64, default='')  # 出版社
    stock = models.IntegerField()  # 库存
    is_deleted = models.BooleanField(default=False)  # 是否删除
    created_at = models.DateTimeField(auto_now_add=True)  # 上架时间

    class Meta(object):
        db_table = 'book_book'
        verbose_name = '图书'


class BorrowRecord(models.Model):
    """
    借阅记录
    """
    book = models.ForeignKey(Book)
    username = models.CharField(max_length=16)  # 借阅人姓名
    borrow_date = models.DateField()  # 借阅日期
    return_date = models.DateField(null=True)  # 归还日期
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_returned(self):
        """
        是否已归还
        """
        return self.return_date is not None

    class Meta(object):
        db_table = 'book_borrow_record'
        verbose_name = '商品'
        verbose_name_plural = '商品'
