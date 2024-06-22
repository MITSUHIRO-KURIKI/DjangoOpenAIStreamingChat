from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
from typing import List, Tuple, Dict, Any

def pagenate_n_validation(per_page_N_items:str     = '25',
                          per_page_N_items_max:int = 100,
                          ) -> str:
    # 意図しない文字列のバリデーション
    try:
        per_page_N_items     = str(per_page_N_items)
        per_page_N_items_int = int(per_page_N_items)
    except:
        per_page_N_items     = '25'
        per_page_N_items_int = int(per_page_N_items)
    # 意図しない範囲のバリデーション
    if per_page_N_items_int > per_page_N_items_max:
        per_page_N_items = str(per_page_N_items_max)
    elif per_page_N_items_int < 1:
        per_page_N_items = '1'
    return per_page_N_items

def get_pagenate_objs_and_range_list(objects:List[Any],
                                     request_page:int     = 1,
                                     per_page_N_items:str = '25',
                                     *,
                                     per_page_N_items_max:int = 100,
                                     on_each_side:int         = 2,
                                     on_ends:int              = 1,
                                     ) -> Tuple[Page, List[str], Dict[str, int]]:
    """
    ページネーションされたオブジェクトリスト、ナビゲーション用のページ範囲リスト、
    およびナビゲーションページ情報を含む辞書を返します。

    Args:
        objects:          ページネーションするオブジェクトのリスト。
        request_page:     表示するページ番号。
        per_page_N_items: 1ページあたりのアイテム数。
        on_each_side:     中央のページ番号の前後に表示するページ数。
        on_ends:          ナビゲーションの端に表示するページ数。

    Returns:
        pagenate_objs:          ページネーションされたオブジェクトのページ。
        pagenate_nav_list:      ナビゲーション用のページ範囲リスト。
        pagenate_nav_page_dict: 前ページ、次ページ、総ページ数を含む辞書。
    """

    per_page_N_items = pagenate_n_validation(per_page_N_items, per_page_N_items_max)
        
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