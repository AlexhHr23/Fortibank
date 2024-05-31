from django.shortcuts import redirect

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Si la respuesta es un error 404 (página no encontrada)
        if response.status_code == 404:
            # Verifica si la URL solicitada comienza con 'admin/'
            if request.path.startswith('/admin'):
                # Permite el acceso a la ruta /admin/
                return response

            # Redirige al dashboard principal en otros casos
            return redirect('account:dashboard')

        return response
