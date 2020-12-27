
from testy import (
    assertEqual,
    assertRaises,
    cli,
)

from __init__ import (
    Anchor,
    Div,
)

###############################################################################
# Helpers
###############################################################################

assertYields = lambda ins, expected: assertEqual(''.join(ins()), expected)

###############################################################################
# Test Single Element Classes
###############################################################################

def test_missing_required_attrs():
    assertRaises(AssertionError, Anchor)

def test_escaped_attr_value():
    assertYields(Anchor(href='http://"example".com'),
"""<a href="http://&quot;example&quot;.com">
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

def test_present_required_attrs():
    assertYields(Anchor(href='http://example.com'),
"""<a href="http://example.com">
</a>
""")

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


if __name__ == '__main__':
    cli(globals())
