# books/middleware/first_middleware.py

class FirstMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Обработка запроса
        print("Привет!")

        # Передача запроса дальше в цепочке middleware
        response = self.get_response(request)

        # Обработка ответа
        print("Пока!")
        return response
