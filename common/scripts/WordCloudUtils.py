from base64 import b64encode
from io import BytesIO
from itertools import chain
from typing import List
from wordcloud import WordCloud

def create_wordcloud(sentence_in_words:List[List[str]],
                     font_path:str           = None,
                     stopwords:List[str]     = [],
                     include_numbers:bool    = True,
                     include_one_char:bool   = True,
                     collocations:bool       = False,
                     max_words:int           = 100,
                     image_width:int         = 1294,
                     image_height:int        = 800,
                     min_font_size:int       = 5,
                     prefer_horizontal:float = .9,
                     colormap:str            = 'tab20',
                     background_color:str    = 'rgb(241,243,244)', # --graph-plot-bg-color
                     image_type:str          = 'png') -> str:
    """
    ### colormap:
     * https://matplotlib.org/stable/users/explain/colors/colormaps.html
    """
    
    words     = list(chain.from_iterable(sentence_in_words))
    words_str = " ".join(words)
    
    word_cloud = WordCloud(font_path         = font_path,
                           stopwords         = set(stopwords),
                           include_numbers   = include_numbers,
                           regexp            = r"[\w']+" if include_one_char else None,
                           collocations      = collocations,
                           max_words         = max_words,
                           width             = image_width,
                           height            = image_height,
                           min_font_size     = min_font_size,
                           prefer_horizontal = prefer_horizontal,
                           colormap          = colormap,
                           background_color  = background_color, 
                           ).generate(words_str)
    
    
    buffer = BytesIO()
    word_cloud.to_image().save(buffer, image_type)
    image_byte  = b64encode(buffer.getvalue())
    image_b64   = image_byte.decode('utf-8')
    img_src_str = f'data:image/{image_type};base64,{image_b64}'
    
    return img_src_str