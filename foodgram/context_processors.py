def get_url_filters(request):
    tags_list = request.GET.getlist('filters')
    filters_url = '&filters=' + '&filters='.join(tags_list)

    return {'filters_url': filters_url} if tags_list else {}
