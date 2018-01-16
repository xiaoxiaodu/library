# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as book_models

COUNT_PER_PAGE = 50


class BorrowRecords(resource.Resource):
    """
    借阅记录列表
    """
    app = 'book'
    resource = 'borrow_records'

    @login_required
    def get(request):
        c = RequestContext(request, {})
        return render_to_response('book/borrow_records.html', c)

    @login_required
    def api_get(request):
        """
        响应API GET
        """
        username = request.GET.get('username')
        bookname = request.GET.get('bookname')
        status = request.GET.get('status', 0)
        params = {}
        if username:
            params['username__icontains'] = username
        if bookname:
            params['book__name__icontains'] = bookname
        if int(status) == 1:
            params['return_date__isnull'] = True
        elif int(status) == -1:
            params['return_date__isnull'] = False
        borrow_records = book_models.BorrowRecord.objects.filter(**params).order_by('-borrow_date')
        
        # 进行分页
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, borrow_records = paginator.paginate(borrow_records, cur_page, count_per_page)

        items = []
        for borrow_record in borrow_records:
            items.append({
                'id': borrow_record.id,
                'bookname': borrow_record.book.name,
                'username': borrow_record.username,
                'borrow_date': borrow_record.borrow_date.strftime("%Y-%m-%d"),
                'return_date': borrow_record.return_date.strftime("%Y-%m-%d") if borrow_record.return_date else "",
                'status': u'已归还' if borrow_record.is_returned else u'出借中',
                'is_returned': borrow_record.is_returned
            })

        response_data = {
            'items': items,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': 'id'
        }

        response = create_response(200)
        response.data = response_data
        return response.get_response()
