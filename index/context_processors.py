def language_context(request):
    return {
        'cur_lang': request.LANGUAGE_CODE,
    }