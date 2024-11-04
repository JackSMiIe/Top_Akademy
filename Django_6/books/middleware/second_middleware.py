# books/middleware/second_middleware.py

class SecondMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                print(f"Вас зовут {request.user.username}")
            else:
                print("Неизвестный посетитель")
        else:
            print("Неизвестный посетитель")

        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Метод для обработки исключений
        print(f"Произошло исключение: {exception}")
        return None  # Возвращение None позволяет другим middleware и Django обработать исключение
