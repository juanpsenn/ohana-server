from app.models import Category


def list_categories():
    return Category.objects.all()
