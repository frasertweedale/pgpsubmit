import abc


class Element(object):
    """An object representing an HTML element and contents."""

    @property
    def tag(self):
        return type(self).__name__.lower()

    @property
    def empty(self):
        return False

    def __init__(self, *args, **kwargs):
        """Initialise the tag.

        Keyword args are attributes.  Args are the initial children, in
        the order given.
        """
        self._children = list(args)
        self._attrs = kwargs

    def add_child(self, child):
        if self.empty:
            raise TypeError('cannot add child to empty element')
        self._children.append(child)

    def __iter__(self):
        if self.empty:
            yield '<{}{}{}/>'.format(
                self.tag,
                ' ' if self._attrs else '',
                ' '.join(
                    '{}="{}"'.format(k, v)
                    for k, v in self._attrs.viewitems()
                )
            )
            return
        yield '<{}{}{}>'.format(
            self.tag,
            ' ' if self._attrs else '',
            ' '.join(
                '{}="{}"'.format(k, v)
                for k, v in self._attrs.viewitems()
            )
        )
        for child in self._children:
            if isinstance(child, Element):
                for _child in child:
                    yield _child
            else:
                yield child
        yield '</{}>'.format(self.tag)


class EmptyElement(Element):
    """Convenience class that defines an empty element."""
    @property
    def empty(self):
        return True


class Html(Element):
    pass


class Head(Element):
    pass


class Title(Element):
    pass


class Body(Element):
    pass


class Br(EmptyElement):
    pass


class Div(Element):
    pass


class H1(Element):
    pass


class H2(Element):
    pass


class H3(Element):
    pass


class Ul(Element):
    pass


class Li(Element):
    pass


class Form(Element):
    pass


class Textarea(Element):
    pass


class Input(EmptyElement):
    pass
