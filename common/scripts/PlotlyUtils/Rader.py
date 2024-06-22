import plotly.graph_objects as go
from ..PythonCodeUtils import insert_br_multi_lines_optimized

def get_go_rader_graph(data_list,
                       *,
                       div_id:str          = 'PlotlyGraph',
                       title:str           = None,
                       mode:str            = 'lines+markers',
                       margin:dict         = {'t': 0, "b": 0, 'l': 80, 'r': 80},
                       to_image_width:int  = 1280,
                       to_image_height:int = 720):
    """
    ## Args: 
    ### data_list: list[Dict[str, Union[str, list[Union[int, float]], list[Union[str, Any]]] ]]
    #### data_list[0]['name']: str
    * 表示名
    #### data_list[0]['r_list']: list[Union[int, float]]
    * 数値リスト
    #### data_list[0]['theta_list']: list[Union[str, Any]]
    * カテゴリ名リスト
    ### div_id
    * 表示ページ中の一意なグラフid
    ### title:
    * グラフのタイトル
    ## to_image_width, to_image_height
    * 保存画像のサイズ
    """
    try:
        fig = go.Figure()
        
        for data in data_list:
            fig.add_trace(go.Scatterpolar(
                r             = data['r_list'],
                theta         = [insert_br_multi_lines_optimized(str(c)) for c in data['theta_list']],
                name          = data['name'],
                meta          = data['name'],
                fill          = 'tonext',
                mode          = mode, # 'lines' or 'markers' or 'text' +combination
                marker        = {'size': 5,},
                opacity       = 0.6,
                hovertemplate = "<b>%{meta}</b><br>%{theta}<br>値: %{r:.1f}<extra></extra>",
            ))
        # plotly.graph_objects グラフの作成△
        # 見た目処理▽
        base_font_size = 15
        base_bg_color  = 'rgb(248,249,250)' # --bs-light
        graph_bg_color = 'rgb(241,243,244)'
        hover_bg_color = base_bg_color
        text_color     = '#343A40'          # --bs-gray-dark
        line_color     = text_color
        # ベース設定
        fig.update_layout(
            font = {
                'size':  base_font_size*.7,
                'color': text_color,
            },
            font_family   = '"Noto Sans JP", "Noto Sans", Arial, Roboto, sans-serif, "Segoe UI"',
            plot_bgcolor  = graph_bg_color,
            paper_bgcolor = base_bg_color,
            autosize      = True,
            margin        = margin,
            margin_autoexpand = True,
        )
        # グラフタイトル
        if title:
            fig.update_layout( title = {
                'text':    title,
                'font': {
                    'size':  base_font_size*.9,
                    'color': text_color,
                },
                'xref':    'container', # 'container', 'paper'
                'x':       .5,
                'y':       .95,
                'xanchor': 'center',}
            )
        # 凡例
        fig.update_layout(
            showlegend = True,
            legend     = {
                'title':      None,
                'xanchor':    'left',
                'yanchor':    'bottom',
                'x':           0,
                'y':           1.01,
                'orientation': 'h', # h or v
                'bgcolor':     base_bg_color,
                'bordercolor': base_bg_color,
                'borderwidth': 1,}
        )
        # hover
        fig.update_layout(
            hovermode = 'x unified', # 'x', 'y', 'closest', False, 'x unified', 'y unified'
            hoverlabel = {
                'font': {
                    'size':  base_font_size*.8,
                    'color': text_color,
                },
                'bgcolor':     hover_bg_color,
                'bordercolor': line_color},
        )
        # レーダチャート特有設定
        # https://plotly.com/python/polar-chart/
        fig.update_layout(
            dragmode = False, # レーダだと使いづらい
            polar = dict(
                            radialaxis = dict(
                            visible   = True,
                            range     = [0.5, 5.5],
                            angle     = 90,
                            tickangle = 90,
                        ),
                        angularaxis = dict(
                            direction = 'clockwise',
                            period    = 6,
                        ),
                    ),
        )
        # 見た目処理△
        # modeBarの設定▽
        fig.update_layout( dragmode = 'pan') # https://plotly.com/javascript/reference/#layout-dragmode
        config = {
            'scrollZoom':  True,  # マウスホイールで拡大縮小
            'responsive':  True,  # レスポンス対応
            # ダウンロード画像の設定
            'toImageButtonOptions': {
                'format':   'png', # one of png, svg, jpeg, webp
                'filename': 'plot',
                'width':    to_image_width,
                'height':   to_image_height,
                'scale':    1      #  Multiply title/legend/axis/canvas sizes by this factor
            },
            'displaylogo': False, # plotlyロゴ表示
            'modeBarButtonsToRemove': [
                ## 2D用
                'zoom2d',        # ズームモード
                'pan2d',         # 移動モード
                'select2d',      # 四角形で選択
                'lasso2d',       # ラッソで選択
                'zoomIn2d',      # 拡大
                'zoomOut2d',     # 縮小
                'autoScale2d',   # 自動範囲設定
                'resetScale2d',  # 元の縮尺
                ## 3D用
                'zoom3d',
                'pan3d',
                'orbitRotation',
                'tableRotation',
                'handleDrag3d',
                'resetCameraDefault3d',
                'resetCameraLastSave3d',
                'hoverClosest3d',
                ## Cartesian用
                'hoverClosestCartesian',
                'hoverCompareCartesian',
                ## 地図用
                'zoomInGeo',
                'zoomOutGeo',
                'resetGeo',
                'hoverClosestGeo'
                ## その他
                # 'toImage',       # 画像ダウンロード
                'hoverClosestGl2d',
                'hoverClosestPie',
                'toggleHover',
                'resetViews',
                'sendDataToCloud',
                'toggleSpikelines',
                'resetViewMapbox',
            ]
        }
        # modeBarの設定△
        plot_html = fig.to_html(
                        include_plotlyjs = False,
                        full_html        = False,
                        div_id           = div_id,
                        config           = config,
                    )
    except:
        # 主にDBが空の場合に発生する例外処理
        plot_html = '<div>No Chart</div>'
    return plot_html