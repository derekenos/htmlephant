# HTMLephant
A small and lazy HTML generator library.

## Description
Use Python classes to describe an HTML document, then get a character generator of the rendered output.

## HTMLElement
All specific element classes derive from either `HTMLElement` or `VoidHTMLElement`.

### Constructor
The `HTMLElement` constructor looks like this:
```
HTMLElement(self, text=None, children=None, **attrs)
```
where:
- `text` will be escaped and become the rendered element's `innerText` value
- `children` is either `None` (for `void-type` elements) or a list of element instances to be rendered as children of this instance
- `**attrs` is the element attributes specified as keyword args

### Attribute Keyword Arg Encoding
Some HTML attribute names are not valid Python keyword names, e.g. `class`, `data-count`.

One solution is to pass an unpacked dict:
```
Div(**{'class': 'fancy', 'data-count': 1})
```

Another solution is to encode the keyword name in a Python-friendly way as described below.

Adding a leading underscore (`'_'`) char to the keyword name signals that the key should be escaped before being rendered to HTML, resulting in:
- the first leading underscore being stripped
- all subsequent underscores being replaced with hyphens

Examples:
- you can specify the HTML attribute `class="fancy"` as the keyword arg `_class='fancy'`
- you can specify the HTML attribute `data-count="1"` as the keyword arg `_data_count=1`

## Document from Scratch Example

```
from __init__ import (
    Body,
    Div,
    Head,
    Html,
    Meta,
    Title,
)

# Construct your document using element classes.                                
el = Html(lang='en', children=[
    Head(children=[
	Meta(charset='utf-8'),
	Title('example document'),
    ]),
    Body(children=[
        Div('some text', id="id-1", _class="class-1")
    ])
])

# Invoke the instance to get an HTML character generator
# for it and its children.
gen = el()
```

### Consume a few characters
```
print([next(gen) for _ in range(5)])
```
#### Output
```
['<', 'h', 't', 'm', 'l']
```

### Be overeager and join the characters into a string
```
print(''.join(gen))
```
#### Output
```
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>
      example document
    </title>
  </head>
  <body>
    <div id="id-1" class="class-1">
      some text
    </div>
  </body>
</html>
```

## Use the Document helper

```
from __init__ import (
    Div,
    Document,
    Title,
)

gen = Document(
    head_els=[
        Title('example document'),
    ],
    body_els=[
        Div('some text', id="id-1", _class="class-1")
    ]
)

print(''.join(gen))
```
### Output
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>
      example document
    </title>
  </head>
  <body>
    <div id="id-1" class="class-1">
      some text
    </div>
  </body>
</html>
```
