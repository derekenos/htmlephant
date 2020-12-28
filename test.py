
from testy import (
    assertEqual,
    assertNone,
    assertRaises,
    cli,
)

from __init__ import (
    Anchor,
    Br,
    Div,
    Document,
    HTMLElement,
    Script,
    Span,
    Textarea,
)

###############################################################################
# Helpers
###############################################################################

_join = ''.join
assertYields = lambda ins, expected: assertEqual(_join(ins()), expected)

###############################################################################
# Misc Tests
###############################################################################

def test_python_version():
    from sys import version_info
    major, minor = version_info[:2]
    if  major < 3 or minor < 6:
        raise AssertionError(
            'Tests require Python >= 3.6 for its kwargs order preservation, '
            f'you\'re using: {major}.{minor}'
        )

###############################################################################
# Encoding / Escaping Method Tests
###############################################################################

def test_encode_attr_key_no_underscores():
    assertEqual(_join(HTMLElement.encode_attr_key('testkey')), 'testkey')

def test_encode_attr_key_escaped():
    assertEqual(_join(HTMLElement.encode_attr_key('__test_key')), '-test-key')

def test_encode_attr_key_not_escaped():
    assertEqual(_join(HTMLElement.encode_attr_key('-_test_key')), '-_test_key')

def test_encode_attr_value_with_double_quotes():
    assertEqual(_join(HTMLElement.encode_attr_value('"x"')), '&quot;x&quot;')

def test_escape_text():
    assertEqual(_join(HTMLElement.escape_text('<html>')), '&lt;html&gt;')

###############################################################################
# Element Attribute Tests
###############################################################################

def test_missing_required_attrs():
    assertRaises(AssertionError, Anchor)

def test_present_required_attrs():
    assertYields(Anchor(href='http://example.com'),
"""<a href="http://example.com">
</a>
""")

def test_multiple_attrs():
    assertYields(Anchor(href='http://example.com', id='some-id'),
"""<a href="http://example.com" id="some-id">
</a>
""")

def test_attr_key_with_leading_underscore():
    assertYields(Div(_class="container"),
"""<div class="container">
</div>
""")

def test_attr_key_with_leading_and_subsequent_underscore():
    assertYields(Div(_data_count=1),
"""<div data-count="1">
</div>
""")

def test_escaped_attr_value():
    assertYields(Anchor(href='http://"example".com'),
"""<a href="http://&quot;example&quot;.com">
</a>
""")

###############################################################################
# Element Text Tests
###############################################################################

def test_nonvoid_no_text():
    assertYields(Anchor(href='http://example.com'),
"""<a href="http://example.com">
</a>
""")

def test_nonvoid_with_text():
    assertYields(Anchor('sample text', href='http://example.com'),
"""<a href="http://example.com">
  sample text
</a>
""")

def test_nonvoid_with_escaped_text():
    assertYields(Anchor('sample <text>', href='http://example.com'),
"""<a href="http://example.com">
  sample &lt;text&gt;
</a>
""")

def test_void_no_text():
    assertYields(Br(),
"""<br>
""")

def test_void_with_text():
    assertRaises(AssertionError, Br, 'abcd')

###############################################################################
# Element Children Tests
###############################################################################

def test_void_children_is_none():
    assertNone(Br().children)

def test_single_child():
    assertYields(Div(children=(Span(),)),
"""<div>
  <span>
  </span>
</div>
""")

def test_lots_of_complicated_kids():
    assertYields(Div(children=[
        Span(f'{i}', id=i, _class=f'style-{i}', children=(Span(f'{i + 1}'),))
        for i in range(3)
    ]),
"""<div>
  <span id="0" class="style-0">
    0
    <span>
      1
    </span>
  </span>
  <span id="1" class="style-1">
    1
    <span>
      2
    </span>
  </span>
  <span id="2" class="style-2">
    2
    <span>
      3
    </span>
  </span>
</div>
""")

def test_appending_children():
    el = Div()
    el.children.append(Span('0'))
    el.children[0].children.append(Span('1'))
    assertYields(el,
"""<div>
  <span>
    0
    <span>
      1
    </span>
  </span>
</div>
""")

###############################################################################
# Document Tests
###############################################################################

def test_empty_document():
    assertEqual(''.join(Document(())),
"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
  <body>
  </body>
</html>
""")

def test_nonempty_document():
    assertEqual(''.join(Document(
        body_els=(Span('abcd'),),
        head_els=(Script('console.log("hello")'),)
    )),
"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <script>
      console.log("hello")
    </script>
  </head>
  <body>
    <span>
      abcd
    </span>
  </body>
</html>
""")

#### Test no text indent

def test_no_text_indent():
    assertYields(Textarea('abcd'),
"""<textarea>
abcd
</textarea>
""")


if __name__ == '__main__':
    cli(globals())
