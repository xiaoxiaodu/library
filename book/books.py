# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as book_models

COUNT_PER_PAGE = 50


class Books(resource.Resource):
    """
    图书列表
    """
    app = 'book'
    resource = 'books'

    def get(request):
        c = RequestContext(request, {
            'is_admin': request.user.is_anonymous() == False,
        })
        return render_to_response('book/books.html', c)
    
    def api_get(request):
        """
        响应API GET
        """
        name = request.GET.get('name')
        author = request.GET.get('author')
        publisher = request.GET.get('publisher')
        status = request.GET.get('status', 0)
        params = {
            'is_deleted': False
        }
        if name:
            params['name__icontains'] = name
        if author:
            params['author__icontains'] = author
        if publisher:
            params['publisher__icontains'] = publisher
        if int(status) == 1:
            params['stock__gt'] = 0
        elif int(status) == -1:
            params['stock'] = 0
        books = book_models.Book.objects.filter(**params).order_by('-id')
        
        # 进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, books = paginator.paginate(books, cur_page, count_per_page)

        items = []
        for book in books:
            items.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'publisher': book.publisher,
                'stock': book.stock,
                'created_at': book.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        response_data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': 'id',
            'is_admin': request.user.is_anonymous() == False
        }

        response = create_response(200)
        response.data = response_data
        return response.get_response()
