from rest_framework.pagination import PageNumberPagination

reserved = ["page", "page_size", "limit", "offset"]


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


def formatted_params(params):
    return {
        key.replace("[]", ""): params.get(key)
        if "[]" not in key
        else params.getlist(key)
        for key in params
        if params.get(key) != "" and key not in reserved
    }
