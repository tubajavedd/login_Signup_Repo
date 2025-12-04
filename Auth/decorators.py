from django.http import JsonResponse

def csrf_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST" and not request.META.get("CSRF_COOKIE"):
            return JsonResponse({"error": "CSRF token missing!"}, status=403)
        return view_func(request, *args, **kwargs)
    return wrapper
