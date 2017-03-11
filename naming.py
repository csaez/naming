import string

tokens = dict()
rule = "{description}_{side}_{type}"


def add_token(name, **kwds):
    if len(kwds) == 0:
        tokens[name] = None
        return True
    if kwds.get("default"):
        kwds["_default"] = kwds["default"]
        del kwds["default"]
    tokens[name] = kwds
    return True

def flush_tokens():
    tokens.clear()
    return True

def remove_token(name):
    if tokens.get(name):
        del tokens[name]
        return True
    return False


def solve(*args, **kwds):
    i = 0
    values = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    for f in fields:
        lookup = tokens[f]
        if lookup is None:  # required
            if kwds.get(f) is not None:
                values[f] = kwds[f]
                continue
            values[f] = args[i]
            i += 1
            continue
        values[f] = lookup[kwds.get(f, "_default")]
    return rule.format(**values)


def parse(name):
    retval = dict()
    fields = [x[1] for x in string.Formatter().parse(rule)]
    split_name = name.split("_")
    for i, f in enumerate(fields):
        value = split_name[i]
        lookup = tokens[f]
        if lookup is None:  # required
            retval[f] = value
            continue
        for k, v in lookup.iteritems():
            if v == value and k != "_default":
                retval[f] = k
                continue
    return retval
