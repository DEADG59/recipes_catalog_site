from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def Pagination(pages_both_sides: int, paginator: Paginator, page_number: str) -> dict:
    '''
    pages_both_sides - кол-во показываемых номеров страниц до и после текущего номера страницы
    page_number - номер текущей страницы
    '''
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, выдать первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если page_number вне диапозона, выдать последнюю страницу
        page_obj = paginator.page(paginator.num_pages)
    page_num = page_obj.number
    page_num_end = paginator.num_pages
    # В зависимости от текущей страницы, определяет какие номера страниц показывать
    if page_num == 1:
        left_pages = []
        right_pages = [i for i in range(2,pages_both_sides+2) if i < page_num_end+1]
    elif page_num == page_num_end:
        left_pages = [i for i in range(page_num_end-pages_both_sides, page_num_end) if i > 0]
        right_pages = []
    else:
        left_pages = [i for i in range(page_num-pages_both_sides, page_num) if i > 0]
        right_pages = [i for i in range(page_num+1, page_num+pages_both_sides+1) if i < page_num_end+1]

    left_pages_more = 1 if 0 < page_num-1-pages_both_sides else 0
    right_pages_more = page_num_end if page_num_end > page_num+pages_both_sides else 0

    return {'page_obj': page_obj,
            'left_pages': left_pages,
            'right_pages': right_pages,
            'left_pages_more': left_pages_more,
            'right_pages_more': right_pages_more}