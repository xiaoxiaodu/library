# -*- coding: utf-8 -*-
import time

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import models as book_models


class Borrow(resource.Resource):
    """
    借阅/归还图书
    """
    app = 'book'
    resource = 'borrow'

    @login_required
    def get(request):
        book_id = request.GET['id']
        book = book_models.Book.objects.get(id=book_id, is_deleted=False)
        c = RequestContext(request, {
            'id': book.id,
            'bookname': book.name,
            'borrow_date': time.strftime("%Y-%m-%d")
        })
        return render_to_response('book/borrow.html', c)

    @login_required
    def api_put(request):
        """
        借书
        """
        book_id = request.POST['id']
        borrow_date = request.POST['borrow_date']
        username = request.POST['username']

        book = book_models.Book.objects.get(id=book_id, is_deleted=False)
        if book.stock > 0:
            book_models.BorrowRecord.objects.create(
                book_id=book_id,
                username=username,
                borrow_date=borrow_date
            )

            # 库存减1
            book.stock = book.stock - 1
            book.save()

            response = create_response(200)
        else:
            response = create_response(500)
            response.errMsg = u'库存不足'
        return response.get_response()

    @login_required
    def api_post(request):
        """
        还书
        """
        borrow_id = request.POST['borrow_id']
        borrow_record = book_models.BorrowRecord.objects.get(id=borrow_id)
        if not borrow_record.is_returned:
            book = borrow_record.book
            book.stock = book.stock + 1
            book.save()

            borrow_record.return_date = time.strftime("%Y-%m-%d")
            borrow_record.save()

        response = create_response(200)
        return response.get_response()
