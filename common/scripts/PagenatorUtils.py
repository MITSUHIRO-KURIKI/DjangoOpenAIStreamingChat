from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def get_pagenate_objs_and_range_list(objects,
                                     request_page:int     = 1,
                                     per_page_N_items:int = 10,
                                     on_each_side:int     = 2,
                                     on_ends:int          = 1,):
    """
    ## Args: 
    ### request_page:
      * 表示するページ
    ### per_page_N_items:
      * 1ページに表示するアイテム数
    ### on_each_side:
      * Pagenation navigation での request_page の前後表示数
    ### on_ends:
      * Pagenation navigation での 末端と末尾の表示数
    """
    paginator = Paginator(objects, per_page_N_items)
    try:
        pagenate_objs = paginator.page(request_page)
    except PageNotAnInteger:
        pagenate_objs = paginator.page(1)
    except EmptyPage:
        pagenate_objs = paginator.page(paginator.num_pages)

    # Pagenation Nav 表示用のリスト
    elided_page_range = pagenate_objs.paginator.get_elided_page_range(request_page, on_each_side=on_each_side, on_ends=on_ends)
    pagenate_nav_list = [ x for x in elided_page_range ]
    # 前後ページ、総ページ
    pagenate_nav_page_dict = {
      'page_count':    paginator.num_pages,
      'previous_page': pagenate_objs.previous_page_number() if pagenate_objs.has_previous() else request_page,
      'next_page':     pagenate_objs.next_page_number()     if pagenate_objs.has_next()     else request_page,
    }

    return pagenate_objs, pagenate_nav_list, pagenate_nav_page_dict