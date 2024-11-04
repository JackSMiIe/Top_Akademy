# books/context_processors/menu.py
def menu_items(request):
    return {
        'menu_items': [
            {'title': 'Главная', 'url_name': 'home'},
            {'title': 'Список авторов', 'url_name': 'author_list'},
        ]
    }
