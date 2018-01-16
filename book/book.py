# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import models as book_models


class Book(resource.Resource):
    """
    编辑/新增/删除图书
    """
    app = 'book'
    resource = 'book'

    @login_required
    def get(request):
        book_id = request.GET.get('id')
        book_data = None
        if book_id:
            book = book_models.Book.objects.get(id=book_id)
            book_data = {
                'id': book_id,
                'name': book.name,
                'author': book.author,
                'publisher': book.publisher,
                'stock': book.stock
            }

        c = RequestContext(request, {
            'book': book_data
        })
        return render_to_response('book/book.html', c)
    
    @login_required
    def api_put(request):
        """
        新增图书
        """
        name = request.POST.get('name')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        stock = int(request.POST.get('stock'))

        book_models.Book.objects.create(name=name, author=author, publisher=publisher, stock=stock)

        response = create_response(200)
        return response.get_response()

    @login_required
    def api_post(request):
        """
        修改图书信息
        """
        book_id = request.POST.get('id')
        name = request.POST.get('name')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        stock = int(request.POST.get('stock'))

        book_models.Book.objects.filter(id=book_id).update(
            name=name, 
            author=author, 
            publisher=publisher, 
            stock=stock
        )

        response = create_response(200)
        return response.get_response()

    @login_required
    def api_delete(request):
        """
        删除图书
        """
        book_id = request.POST.get('id')

        book_models.Book.objects.filter(id=book_id).update(is_deleted=True)

        response = create_response(200)
        return response.get_response()