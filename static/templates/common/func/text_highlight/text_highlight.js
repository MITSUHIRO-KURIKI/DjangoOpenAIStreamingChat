// Reference
// https://www.nishishi.com/javascript-tips/auto-word-highlighter.html

// 引数
// instruction_obj = { HighlightWords: List[str], subHighlightWords: List[str] }

// 元のHTMLソースを保持しておく変数
var backupElements = new Object();
// 文字列を検索してハイライト用要素を加える処理
function textHighlightReplacer( str, word , att  ) {
    let SearchString  = '(' + word + ')';
    let RegularExp    = new RegExp( SearchString, 'ig' ); // i: 大文字小文字を区別しない, g: グローバル検索
    let ReplaceString = '<span class="' + att + '">$1</span>';
    let ResString     = str.replace( RegularExp , ReplaceString );
    return ResString;
};
// ハイライトを加える
function addTextHighlight( instruction_obj ) {
    let IsObjectEmpty = !Object.keys( backupElements ).length;
    if ( !IsObjectEmpty ) {
        clearTextHighlight();
    };
    elements = document.getElementsByClassName('TextHighlightArea');
    for(var i=0; i<elements.length; i++ ) {
        backupElements[i]     = elements[i].innerHTML;
        let element           = elements[i].innerHTML;
        for (var j = 0; j < instruction_obj['HighlightWords'].length; ++j) {
            element = textHighlightReplacer( element, instruction_obj['HighlightWords'][j],    '0' );
        };
        for (var j = 0; j < instruction_obj['subHighlightWords'].length; ++j) {
            element = textHighlightReplacer( element, instruction_obj['subHighlightWords'][j], '1' );
        };
        elements[i].innerHTML = element
    };
};
// ハイライトを消す
function clearTextHighlight() {
    let IsObjectEmpty = !Object.keys( backupElements ).length;
    if (!IsObjectEmpty) {
        elements = document.getElementsByClassName('TextHighlightArea');
        for(var i=0; i<elements.length; i++ ) {
            elements[i].innerHTML = backupElements[i];
            delete backupElements[i];
        };
    };
};
// 一括ハイライト処理( ボタンクリック等で発火させる場合 )
function RunTextHighlight( instruction_obj ) {
    let IsObjectEmpty = !Object.keys( backupElements ).length;
    if( IsObjectEmpty ) {
        // 何もバックアップされていなければ（未ハイライトなので）ハイライトを加える
        addTextHighlight( instruction_obj );
    } else {
        // 何かバックアップされていれば（ハイライト済みなので）ハイライトを消す
        clearTextHighlight();
    }
};