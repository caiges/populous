import random
from django.contrib.contenttypes.models import ContentType

#  Helper functions
def get_admin_filter_ads():
    list = []
    for model in ContentType.objects.filter(app_label='advertising'):
        #if model.get_model_module().Klass._meta.module_constants.get('ADMIN_FILTER_DISPLAY'):
        #    list.append(model.get_model_module().Klass._meta.module_name)
        list.append('1')
    return list

def windex(lst):
    """
    An attempt to make a random.choose() function that makes weighted choices
    accepts a list of tuples with the item and probability as a pair
    """
    wtotal = sum([x[1] for x in lst])
    n = random.uniform(0, wtotal)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item