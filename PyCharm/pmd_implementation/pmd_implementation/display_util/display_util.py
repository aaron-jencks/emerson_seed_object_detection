from PyQt5.QtCore import Qt


def get_widget_dict(identifier: str, row: int, col: int, tip: str = '') -> dict:

    res = {'id': identifier, 'row': row, 'col': col}

    if tip != '':
        res['tip'] = tip

    return res


def get_text_widg_dict(title: str, identifier: str, row: int, col: int, tip: str = '') -> dict:

    res = get_widget_dict(identifier, row, col, tip)
    res['text'] = title

    return res


def get_slider_widg_dict(orient: Qt.Orientation, identifier: str, row: int, col: int, tip: str = '') -> dict:

    res = get_widget_dict(identifier, row, col, tip)
    res['orient'] = orient

    return res


def get_custom_widg_dict(widg_type, identifier: str, row: int, col: int, tip: str = '', kwargs=None) -> dict:

    if kwargs is None:
        kwargs = {}

    res = get_widget_dict(identifier, row, col, tip)
    res['type'] = widg_type
    res['kwargs'] = kwargs

    return res
