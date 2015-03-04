import ast


def string_to_list(string_list):
    """ Convert string to list
        u"[{'product_id': 5, 'product_quantity': 12}]"
        [{'product_id': 5, 'product_quantity': 12}]
    """
    try:
        result = ast.literal_eval(string_list)
    except:
        result = []

    return result
