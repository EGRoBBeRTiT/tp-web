from app.models import Tag, Profile


def add_popular_tags(request):
    popular_tags = Tag.objects.get_popular_tags()
    return {'popular_tags': popular_tags}


def add_best_members(request):
    best_members = Profile.objects.get_best_members()
    return {'best_members': best_members}

