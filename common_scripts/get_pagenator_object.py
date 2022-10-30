from django.core.paginator import ( 
    Paginator, EmptyPage, PageNotAnInteger,
)

def get_pagenator_object(data, paginate_by, page):
    paginator = Paginator(data, paginate_by)
    try: OBJECT = paginator.page(page)
    except PageNotAnInteger: OBJECT = paginator.page(1)
    except EmptyPage: OBJECT = paginator.page(1)
    return OBJECT