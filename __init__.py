"""HTMLephant - A small and lazy HTML generator.
"""

###############################################################################
# Constants
###############################################################################

DOCTYPE = '<!DOCTYPE html>\n'

class Entities:
    DOUBLE_QUOTE = '&quot;'
    GREATER_THAN = '&gt;'
    LESS_THAN = '&lt;'

###############################################################################
# HTMLElement Base Class
###############################################################################

class HTMLElement:
    # Specify whether this is a void-type element which is self-closing and
    # prohibited from text content or children.
    IS_VOID = False

    # Specify the names of any of attributes that must be specified when
    # instantiating this element.
    REQUIRED_ATTRS = ()

    # Specify whether the text content of this element should be indented
    # along with its tags.
    INDENT_TEXT = True

    # Specify whether to escape the text.
    ESCAPE_TEXT = True

    # Specify the number of spaces to indent this element's children.
    CHILD_INDENT = 2

    def __init__(self, text=None, children=None, **attrs):
        # Assert that TAG_NAME is defined.
        if not hasattr(self, 'TAG_NAME'):
            raise AssertionError('Please subclass HTMLElement and define a '
                                 'TAG_NAME attribute')
        # Assert that text and children are None for a void-type element.
        if self.IS_VOID and (text or children is not None):
            raise AssertionError(
                'text and children are prohibited for void tag "{}"'
                .format(self.TAG_NAME)
            )
        # Assert that all required attributes were specified.
        if any(k not in attrs for k in self.REQUIRED_ATTRS):
            raise AssertionError(
                'missing required attrs {} for tag "{}"'.format(
                    [k for k in self.REQUIRED_ATTRS if k not in attrs],
                    self.TAG_NAME
                )
            )
        # Save the text content value.
        self.text = text
        # Save the attributes dict.
        self.attrs = attrs
        # Save the child list.
        self.children = None if self.IS_VOID else (children or [])

    @staticmethod
    def encode_attr_key(k):
        """
        Yield the attribute key with any leading underscore stripped (to
        provide for the specification of attribute name keyword arguments that
        would otherwise collide with a Python keyword, e.g. class) and, if a
        leading underscore is present, replace all following underscores with
        a hyphens (to provide for the specification of attribute names
        containing a hyphen which is standard HTML stuff). Note that both of
        these cases could be handled with an unpacked dict as the kwargs,
        i.e. func(**{'class': '...', 'data-count': 1}), but that's a lot of
        extra characters.
        """
        escaped = k[0] == '_'
        i = 1 if escaped else 0
        k_len = len(k)
        while i < k_len:
            c = k[i]
            if c == '_' and escaped:
                yield '-'
            else:
                yield c
            i += 1

    @staticmethod
    def encode_attr_value(v):
        """
        Yield the attribute value with any double-quotes replaced with the
        corresponding HTML entity.
        """
        for c in str(v):
            if c == '"':
                yield from Entities.DOUBLE_QUOTE
            else:
                yield c

    @staticmethod
    def escape_text(text):
        """
        Yield text with any offending character replaced with its corresponding
        HTML entity.
        """
        for c in text:
            if c == '<':
                yield from Entities.LESS_THAN
            elif c == '>':
                yield from Entities.GREATER_THAN
            else:
                yield c

    @staticmethod
    def _pad_gen(num):
        """Yield the specified number of SPACE characters.
        """
        while num > 0:
            yield ' '
            num -= 1

    def html(self, indent=0):
        """
        Yield the HTML characters that comprise this element and all of its
        children.
        """
        # Yield the start tag.
        yield from self._pad_gen(indent)
        yield '<'
        yield from self.TAG_NAME
        if self.attrs:
            for k, v in self.attrs.items():
                yield ' '
                yield from self.encode_attr_key(k)
                yield '='
                yield '"'
                yield from self.encode_attr_value(v)
                yield '"'
        yield '>'
        yield '\n'

        # Yield the text.
        if self.text:
            text = (self.escape_text(self.text) if self.ESCAPE_TEXT
                    else self.text)
            if not self.INDENT_TEXT:
                yield from text
            else:
                yield from self._pad_gen(indent + self.CHILD_INDENT)
                for c in text:
                    yield c
                    if c == '\n':
                        yield from self._pad_gen(indent + self.CHILD_INDENT)
            yield '\n'

        # Yield the children.
        if self.children:
            for child in self.children:
                yield from child.html(indent + self.CHILD_INDENT)

        # Maybe yield closing tag.
        if not self.IS_VOID:
            yield from self._pad_gen(indent)
            yield '<'
            yield '/'
            yield from self.TAG_NAME
            yield '>'
            yield '\n'

# Define an HTMLElemnt subclass from which to derive void elements.
class VoidHTMLElement(HTMLElement):
    IS_VOID = True

# Define a NOEL (No-Element) class that implements a static html() method that
# allows it to be used wherever a normal element can appear, but which yields
# only a single empty string. This is useful for inline conditionals, e.g.
# x = Element(<variable>) if <variable> else NOEL
class NOEL():
    @staticmethod
    def html(indent=None):
        yield ''

###############################################################################
# Common Element Subclasses
###############################################################################

class Anchor(HTMLElement):
    TAG_NAME = 'a'
    REQUIRED_ATTRS = ('href',)

class Body(HTMLElement):
    TAG_NAME = 'body'

class Br(VoidHTMLElement):
    TAG_NAME = 'br'

class Button(HTMLElement):
    TAG_NAME = 'button'

class Div(HTMLElement):
    TAG_NAME = 'div'

class Form(HTMLElement):
    TAG_NAME = 'form'

class H1(HTMLElement):
    TAG_NAME = 'h1'

class H2(HTMLElement):
    TAG_NAME = 'h2'

class H3(HTMLElement):
    TAG_NAME = 'h3'

class H4(HTMLElement):
    TAG_NAME = 'h4'

class H5(HTMLElement):
    TAG_NAME = 'h5'

class H6(HTMLElement):
    TAG_NAME = 'h6'

class Html(HTMLElement):
    TAG_NAME = 'html'
    REQUIRED_ATTRS = ('lang',)

class Hr(VoidHTMLElement):
    TAG_NAME = 'hr'

class Head(HTMLElement):
    TAG_NAME = 'head'

class Img(VoidHTMLElement):
    TAG_NAME = 'img'
    REQUIRED_ATTRS = ('src', 'alt')

class Input(VoidHTMLElement):
    TAG_NAME = 'input'
    REQUIRED_ATTRS = ('type',)

class Label(HTMLElement):
    TAG_NAME = 'label'
    REQUIRED_ATTRS = ('for',)

class Li(HTMLElement):
    TAG_NAME = 'li'

class Meta(VoidHTMLElement):
    TAG_NAME = 'meta'

class Ol(HTMLElement):
    TAG_NAME = 'ol'

class Option(HTMLElement):
    TAG_NAME = 'option'
    REQUIRED_ATTRS = ('value',)

class Paragraph(HTMLElement):
    TAG_NAME = 'p'

class Script(HTMLElement):
    TAG_NAME = 'script'
    ESCAPE_TEXT = False

class Select(HTMLElement):
    TAG_NAME = 'select'

class Source(VoidHTMLElement):
    TAG_NAME = 'source'

class Span(HTMLElement):
    TAG_NAME = 'span'

class Strong(HTMLElement):
    TAG_NAME = 'strong'

class Style(HTMLElement):
    TAG_NAME = 'style'
    ESCAPE_TEXT = False

class Table(HTMLElement):
    TAG_NAME = 'table'

class Tbody(HTMLElement):
    TAG_NAME = 'tbody'

class Td(HTMLElement):
    TAG_NAME = 'td'

class Template(HTMLElement):
    TAG_NAME = 'template'

class Textarea(HTMLElement):
    TAG_NAME = 'textarea'
    INDENT_TEXT = False

class Th(HTMLElement):
    TAG_NAME = 'th'

class Thead(HTMLElement):
    TAG_NAME = 'thead'

class Title(HTMLElement):
    TAG_NAME = 'title'

class Tr(HTMLElement):
    TAG_NAME = 'tr'

class Ul(HTMLElement):
    TAG_NAME = 'ul'

###############################################################################
# GenReader Class
###############################################################################

class GenReader:
    """
    A file-like character generator wrapper/encoder that implements readinto().
    """
    def __init__(self, gen, encoding='utf-8'):
        self.gen = gen
        self.encoding = encoding

    def readinto(self, buf):
        # Write up to len(buf) bytes into buf from the generator and return the
        # number of bytes written.
        i = 0
        buf_size = len(buf)
        while i < buf_size:
            try:
                char = next(self.gen)
            except StopIteration:
                break
            for byte in char.encode(self.encoding):
                buf[i] = byte
                i += 1
        return i

###############################################################################
# Document Function
###############################################################################

def Document(body_els, head_els=()):
    """
    Yield an HTML document that comprises the specified body and head child
    elements.
    """
    yield from DOCTYPE
    yield from Html(
        lang='en',
        children=(
            Head(
                children=(
                    Meta(charset='utf-8'),
                    Meta(
                        name='viewport',
                        content='width=device-width, initial-scale=1'
                    )
                )
                + tuple(head_els)
            ),
            Body(children=body_els)
        )
    ).html()

# Define a GenReader-wrapped version of Document.
DocumentStream = lambda *args, **kwargs: GenReader(Document(*args, **kwargs))
