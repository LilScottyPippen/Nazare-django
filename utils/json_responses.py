from django.http import JsonResponse


def success_response(message, status=200):
    return JsonResponse({'status': 'success', 'message': message}, status=status)


def error_response(message, status=500):
    return JsonResponse({'status': 'error', 'message': message}, status=status)
