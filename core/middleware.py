from django.shortcuts import redirect


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Si la respuesta es un error 404 (página no encontrada)
        if response.status_code == 404:
            # Redirige al dashboard principal
            return redirect('account:dashboard')

        return response