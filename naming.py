_tokens = dict()
_rules = {"_active": None}


class Token(object):
    def __init__(self, name):
        super(Token, self).__init__()
        self._name = name
        self._default = None
        self._items = dict()

    def set_default(self, value):
        self._default = value

    def default(self):
        if self._default is None and len(self._items):
            self._default = self._items.values()[0]
        return self._default

    def add_item(self, name, value):
        self._items[name] = value

    def is_required(self):
        return self.default() is None

    def solve(self, name=None):
        if name is None:
            return self.default()
        return self._items.get(name)

    def parse(self, value):
        for k, v in self._items.iteritems():
            if v == value:
                return k


class Rule(object):
    def __init__(self, name):
        super(Rule, self).__init__()
        self._name = name
        self._fields = list()

    def fields(self):
        return tuple(self._fields)

    def add_fields(self, token_names):
        self._fields.extend(token_names)
        return True

    def _pattern(self):
        return "{{{}}}".format("}_{".join(self._fields))

    def solve(self, **values):
        return self._pattern().format(**values)

    def parse(self, name):
        retval = dict()
        split_name = name.split("_")
        for i, f in enumerate(self.fields()):
            value = split_name[i]
            token = _tokens[f]
            if token.is_required():
                retval[f] = value
                continue
            retval[f] = token.parse(value)
        return retval


def add_rule(name, *fields):
    rule = Rule(name)
    rule.add_fields(fields)
    _rules[name] = rule
    if active_rule() is None:
        set_active_rule(name)
    return True

def flush_rules():
    _rules.clear()
    _rules["_active"] = None
    return True

def remove_rule(name):
    if has_rule(name):
        del _rules[name]
        return True
    return False

def has_rule(name):
    return name in _rules.keys()

def active_rule():
    k = _rules["_active"]
    return _rules.get(k)

def set_active_rule(name):
    if not has_rule(name):
        return False
    _rules["_active"] = name
    return True


def add_token(name, **kwds):
    token = Token(name)
    for k, v in kwds.iteritems():
        if k == "default":
            token.set_default(v)
            continue
        token.add_item(k, v)
    _tokens[name] = token
    return token

def flush_tokens():
    _tokens.clear()
    return True

def remove_token(name):
    if has_token(name):
        del _tokens[name]
        return True
    return False

def has_token(name):
    return name in _tokens.keys()


def solve(*args, **kwds):
    i = 0
    values = dict()
    rule = active_rule()
    for f in rule.fields():
        token = _tokens[f]
        if token.is_required():
            if kwds.get(f) is not None:
                values[f] = kwds[f]
                continue
            values[f] = args[i]
            i += 1
            continue
        values[f] = token.solve(kwds.get(f))
    return rule.solve(**values)


def parse(name):
    rule = active_rule()
    return rule.parse(name)
