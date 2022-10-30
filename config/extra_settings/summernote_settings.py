# SETTINGS django-summernote
SUMMERNOTE_THEME = 'bs4'
X_FRAME_OPTOPNS = 'SAMEORIGIN'
SUMMERNOTE_CONFIG = {
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '500px',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript', 'strikethrough', 'clear']],
            # ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['hr', 'link', 'picture', 'video']],
            ['view', ['fullscreen', 'help', 'codeview']],
        ],
    },
    'iframe': True,
    'attachment_require_authentication': True,
    'js': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/codemirror.js',
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/mode/xml/xml.js',
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/2.36.0/formatting.js',
    ),
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/codemirror.css',
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/3.20.0/theme/monokai.css',
    ),
    'codemirror': {
        'mode': 'htmlmixed',
        'lineNumbers': 'true',
        # You have to include theme file in 'css' or 'css_for_inplace' before using it.
        'theme': 'monokai',
    },
}
SUMMERNOTE_HELPER = '\
        <div class="badge badge-pill badge-info" data-toggle="collapse" href="#MultiCollapse-summernote" aria-expanded="false" aria-controls="MultiCollapse-summernote">summernote helper<i class="bi bi-arrows-expand ml-2"></i></div>\
        <div class="collapse multi-collapse" id="MultiCollapse-summernote">\
        <div class="list-group list-group-flush mx-3 my-0 p-0">\
        <div class="list-group-item mx-0 my-1 p-0"><kbd>SHIFT</kbd>+<kbd>ENTER</kbd> :装飾を残したまま改行</div>\
        <div class="list-group-item mx-0 my-1 p-0"><kbd>@</kbd>+<kbd>any words</kbd> :メンション</div>\
        <div class="list-group-item mx-0 my-1 p-0"><kbd>:</kbd>+<kbd>alphabet</kbd> :絵文字 [ <a class="link-info text-decoration-none" href="https://github.com/ikatyang/emoji-cheat-sheet/" target="_blank" rel="noopener"><i class="bi bi-box-arrow-up-right"></i>cheat sheet</a> ]</div>\
        </div></div>'