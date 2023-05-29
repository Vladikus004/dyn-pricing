def find(element, json):
    keys = element.split('/')
    rv = json
    for key in keys:
        if rv is None:
            return None
        if key.isdigit():
            key = int(key)
            rv = rv[key]
        elif key in rv:
            rv = rv[key]
        else:
            # print("not found")
            return None
    return rv
