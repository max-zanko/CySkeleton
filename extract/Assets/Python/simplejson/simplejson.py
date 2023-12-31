r"""
A simple, fast, extensible JSON encoder and decoder

JSON (JavaScript Object Notation) <http://json.org> is a subset of
JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data
interchange format.

simplejson exposes an API familiar to uses of the standard library
marshal and pickle modules.

Encoding basic Python object hierarchies::
    
    >>> import simplejson
    >>> simplejson.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    '["foo", {"bar":["baz", null, 1.0, 2]}]'
    >>> print simplejson.dumps("\"foo\bar")
    "\"foo\bar"
    >>> print simplejson.dumps(u'\u1234')
    "\u1234"
    >>> print simplejson.dumps('\\')
    "\\"
    >>> from StringIO import StringIO
    >>> io = StringIO()
    >>> simplejson.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]'

Decoding JSON::
    
    >>> import simplejson
    >>> simplejson.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    [u'foo', {u'bar': [u'baz', None, 1.0, 2]}]
    >>> simplejson.loads('"\\"foo\\bar"')
    u'"foo\x08ar'
    >>> from StringIO import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> simplejson.load(io)
    [u'streaming API']

Extending JSONEncoder::
    
    >>> import simplejson
    >>> class ComplexEncoder(simplejson.JSONEncoder):
    ...     def default(self, obj):
    ...         if isinstance(obj, complex):
    ...             return [obj.real, obj.imag]
    ...         return simplejson.JSONEncoder.default(self, obj)
    ... 
    >>> dumps(2 + 1j, cls=ComplexEncoder)
    '[2.0, 1.0]'
    >>> ComplexEncoder().encode(2 + 1j)
    '[2.0, 1.0]'
    >>> list(ComplexEncoder().iterencode(2 + 1j))
    ['[', '2.0', ', ', '1.0', ']']
    

Note that the JSON produced by this module is a subset of YAML,
so it may be used as a serializer for that as well.
"""
__version__ = '1.1'
__all__ = [
    'dump', 'dumps', 'load', 'loads',
    'JSONDecoder', 'JSONEncoder',
]

from simplejson_decoder import JSONDecoder
from simplejson_encoder import JSONEncoder

def dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, **kw):
    """
    Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    If ``skipkeys`` is ``True`` then ``dict`` keys that are not basic types
    (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``) 
    will be skipped instead of raising a ``TypeError``.

    If ``ensure_ascii`` is ``False``, then the some chunks written to ``fp``
    may be ``unicode`` instances, subject to normal Python ``str`` to
    ``unicode`` coercion rules.  Unless ``fp.write()`` explicitly
    understands ``unicode`` (as in ``codecs.getwriter()``) this is likely
    to cause an error.

    If ``check_circular`` is ``False``, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is ``False``, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``)
    in strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg.
    """
    if cls is None:
        cls = JSONEncoder
    iterable = cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan,
        **kw).iterencode(obj)
    # could accelerate with writelines in some versions of Python, at
    # a debuggability cost
    for chunk in iterable:
        fp.write(chunk)

def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, **kw):
    """
    Serialize ``obj`` to a JSON formatted ``str``.

    If ``skipkeys`` is ``True`` then ``dict`` keys that are not basic types
    (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``) 
    will be skipped instead of raising a ``TypeError``.

    If ``ensure_ascii`` is ``False``, then the return value will be a
    ``unicode`` instance subject to normal Python ``str`` to ``unicode``
    coercion rules instead of being escaped to an ASCII ``str``.

    If ``check_circular`` is ``False``, then the circular reference check
    for container types will be skipped and a circular reference will
    result in an ``OverflowError`` (or worse).

    If ``allow_nan`` is ``False``, then it will be a ``ValueError`` to
    serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
    strict compliance of the JSON specification, instead of using the
    JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).

    To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
    ``.default()`` method to serialize additional types), specify it with
    the ``cls`` kwarg.
    """
    if cls is None:
        cls = JSONEncoder
    return cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, **kw).encode(obj)

def load(fp, encoding=None, cls=None, **kw):
    """
    Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a Python object.

    If the contents of ``fp`` is encoded with an ASCII based encoding other
    than utf-8 (e.g. latin-1), then an appropriate ``encoding`` name must
    be specified.  Encodings that are not ASCII based (such as UCS-2) are
    not allowed, and should be wrapped with
    ``codecs.getreader(fp)(encoding)``, or simply decoded to a ``unicode``
    object and passed to ``loads()``
    
    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg.
    """
    if cls is None:
        cls = JSONDecoder
    return cls(encoding=encoding, **kw).decode(fp.read())

def loads(s, encoding=None, cls=None, **kw):
    """
    Deserialize ``s`` (a ``str`` or ``unicode`` instance containing a JSON
    document) to a Python object.

    If ``s`` is a ``str`` instance and is encoded with an ASCII based encoding
    other than utf-8 (e.g. latin-1) then an appropriate ``encoding`` name
    must be specified.  Encodings that are not ASCII based (such as UCS-2)
    are not allowed and should be decoded to ``unicode`` first.

    To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
    kwarg.
    """
    if cls is None:
        cls = JSONDecoder
    return cls(encoding=encoding, **kw).decode(s)

def read(s):
    """
    json-py API compatibility hook.  Use loads(s) instead.
    """
    import warnings
    warnings.warn("simplejson.loads(s) should be used instead of read(s)",
        DeprecationWarning)
    return loads(s)

def write(obj):
    """
    json-py API compatibility hook.  Use dumps(s) instead.
    """
    import warnings
    warnings.warn("simplejson.dumps(s) should be used instead of write(s)",
        DeprecationWarning)
    return dumps(obj)


