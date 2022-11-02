from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template import Library
from django.contrib.admin.views.main import (
    PAGE_VAR,
    # ALL_VAR,
    # ORDER_VAR,
    # SEARCH_VAR,
)

register = Library()
DOT = "."


@register.simple_tag
def custom_paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    # print(cl.paginator.num_pages)
    if i == DOT:
        # return '… '
        return format_html(
            '<li class="paginate_button page-item disabled"><a href="#" class="page-link" disabled>... </a></li>'
        )
    elif i == cl.page_num:
        return format_html(
            '<li class="paginate_button page-item active"><a class="page-link page-link-active" disabled>{}</a></li> ',
            i,
        )
    else:
        return format_html(
            '<li class="paginate_button page-item"><a class="page-link" href="{}" {}>{}</a></li>',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(' class="end"' if i == cl.paginator.num_pages - 1 else ""),
            i,
        )
