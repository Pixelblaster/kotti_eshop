import ast


def string_to_list(string_list):
    """ Convert string to list
    """
    try:
        result = ast.literal_eval(string_list)
    except:
        result = []

    return result
