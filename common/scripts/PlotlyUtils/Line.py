import pandas as pd
import plotly.graph_objects as go
from ..PythonCodeUtils import insert_br_multi_lines_optimized

def get_go_line_graph(data_df:pd.DataFrame        = None,
                      y_col_name:str              = 'year',
                      *,
                      div_id:str                  = 'PlotlyGraph',
                      title:str                   = None,
                      mode:str                    = 'lines+markers+text',
                      margin:dict                 = {'t': 0, "b": 0, 'l': 0, 'r': 0},
                      xaxis_title:str             = 'X',
                      xaxis_tickformat:str        = '%y/%m',
                      xaxis_dtick:float           = 1.0,
                      yaxis_dtick:float           = 1.0,
                      rangeslider_thickness:float = None,
                      to_image_width:int          = 1280,
                      to_image_height:int         = 720):
    """
    ## Args: 
    ### data_df:
    * データ
    ### y_col_name:
    * y軸の格納されたカラム名
    ### div_id
    * 表示ページ中の一意なグラフid
    ### title:
    * グラフのタイトル
    ### xaxis_dtick:
    * x軸 ステップ数
    ### yaxis_dtick:
    * x軸 ステップ数
    ## rangeslider_thickness
    * x軸 レンジスライダーの高さ
    ## to_image_width, to_image_height
    * 保存画像のサイズ
    """
    try:
        fig = go.Figure()

        for col in data_df.columns:
            if col != y_col_name:
                fig.add_trace(go.Scatter(
                    x             = data_df[y_col_name],
                    y             = data_df[col],
                    name          = insert_br_multi_lines_optimized(col),
                    meta          = col,
                    yaxis         = 'y1',
                    mode          = mode, # 'lines' or 'markers' or 'text' +combination
                    marker        = {'size': 5,},
                    opacity       = 0.8,
                    customdata    = data_df[[y_col_name, col]],
                    textposition  = 'top center',
                    texttemplate  = '%{customdata[1]:.1f}',
                    hovertemplate = "%{meta}: %{customdata[1]:.1f}<extra></extra>",
                ))
        # plotly.graph_objects グラフの作成△
        # 見た目処理▽
        base_font_size = 15
        base_bg_color  = 'rgb(248,249,250)' # --bs-light
        graph_bg_color = 'rgb(241,243,244)'
        hover_bg_color = base_bg_color
        text_color     = 'rgb(52,58,64)'  # --bs-gray-dark
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
                'y':       .99,
                'xanchor': 'center',}
            )
        # 凡例
        fig.update_layout(
            showlegend = True,
            legend     = {
                'xanchor':    'left',
                'yanchor':    'top',
                'x':           1,
                'y':           1,
                'orientation': 'v', # h or v
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
        # 軸
        fig.update_layout(
            xaxis = {
                'title':      xaxis_title,
                'tickformat': xaxis_tickformat,
                'tickmode':   'linear',
                'dtick':      xaxis_dtick,
                'autorange':  True,
            },
            yaxis = {
                'tickmode':  'linear',
                'dtick':     yaxis_dtick,
                'autorange': True,
            }
        )
        fig.update_xaxes(
            showline  = False,
            linewidth = 1,
            linecolor = line_color,
            color     = text_color,
        )
        fig.update_yaxes(
            showline  = False,
            linewidth = 1,
            linecolor = line_color,
            color     = text_color,
        )
        # レンジスライダー
        if rangeslider_thickness:
            fig.update_xaxes(
                rangeslider_visible   = True,
                rangeslider_thickness = rangeslider_thickness,
            )
            fig.update_yaxes(
                fixedrange  = False,
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
                #'zoom2d',        # ズームモード
                #'pan2d',         # 移動モード
                'select2d',       # 四角形で選択
                'lasso2d',        # ラッソで選択
                #'zoomIn2d',      # 拡大
                #'zoomOut2d',     # 縮小
                #'autoScale2d',   # 自動範囲設定
                'resetScale2d',   # 元の縮尺
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