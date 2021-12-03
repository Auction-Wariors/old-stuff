from stores.models import Store


def store(request):
    """This middleware injects a Store object to the template if request.user has a store"""
    if request.user.is_anonymous:
        return {'store': 'test'}
    user_has_store = Store.objects.get(owner=request.user)
    return {'store': user_has_store}

