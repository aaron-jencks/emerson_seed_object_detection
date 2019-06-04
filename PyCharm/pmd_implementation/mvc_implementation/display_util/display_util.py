from PyQt5.QtCore import Qt


def get_file_dialog_dict(prompt: str = 'Open file', start_directory: str = '/home', valid_files: str = "All Files(*)"):
    return {'prompt': prompt, 'start_directory': start_directory, 'valid_files': valid_files}


def get_yn_dialog_dict(prompt: str = "???", description: str = "", detailed_text: str = ""):
    return {'prompt': prompt, 'description': description, 'detailed_text': detailed_text}


def get_widget_dict(identifier: str, row: int, col: int, row_span: int = 1, col_span: int = 1, tip: str = '') -> dict:

    res = {'id': identifier, 'row': row, 'col': col, 'rowSpan': row_span, 'columnSpan': col_span}

    if tip != '':
        res['tip'] = tip

    return res


def get_text_widg_dict(title: str, identifier: str,
                       row: int, col: int, row_span: int = 1, col_span: int = 1, tip: str = '') -> dict:

    res = get_widget_dict(identifier, row, col, row_span, col_span, tip)
    res['text'] = title

    return res


def get_text_entry_widg_dict(identifier: str,
                             row: int, col: int, row_span: int = 1, col_span: int = 1, tip: str = '') -> dict:

    res = get_widget_dict(identifier, row, col, row_span, col_span, tip)

    return res


def get_slider_widg_dict(orient: Qt.Orientation, identifier: str,
                         row: int, col: int, row_span: int = 1, col_span: int = 1, tip: str = '') -> dict:

    res = get_widget_dict(identifier, row, col, row_span, col_span, tip)
    res['orient'] = orient

    return res


def get_custom_widg_dict(widg_type, identifier: str,
                         row: int, col: int, row_span: int = 1, col_span: int = 1, tip: str = '', kwargs=None) -> dict:

    if kwargs is None:
        kwargs = {}

    res = get_widget_dict(identifier, row, col, row_span, col_span, tip)
    res['type'] = widg_type
    res['kwargs'] = kwargs

    return res
