from app.models import Like


def like_event(event, user):
    like = Like.objects.filter(event_id=event, user_id=user).last()
    if like:
        like.delete()
    else:
        like = Like.objects.create(event_id=event, user_id=user)
        like.save()

    return like
