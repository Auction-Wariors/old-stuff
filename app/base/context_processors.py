from stores.models import Store


def store(request):
    if request.user.is_anonymous:
        return {'store': 'test'}
    user_has_store = Store.objects.filter(owner=request.user).first()
    owner = user_has_store
    return {'store': owner}

