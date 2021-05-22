def get_current_host( request):
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}/'