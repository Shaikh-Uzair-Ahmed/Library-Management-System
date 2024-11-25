def session_lib_num(request):
    return {'lib_num': request.session.get('lib_num', None)}