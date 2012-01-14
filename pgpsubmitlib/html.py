# This file is part of pgpsubmit
# Copyright (C) 2011 Fraser Tweedale
#
# pgpsubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pgpsubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pgpsubmit.  If not, see <http://www.gnu.org/licenses/>.

import cgi


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
                '{}="{}"'.format(k, cgi.escape(str(v), True))
                for k, v in self._attrs.viewitems()
            )
        )
        for child in self._children:
            if isinstance(child, Element):
                for _child in child:
                    yield _child
            else:
                yield cgi.escape(str(child))
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


class Hr(EmptyElement):
    pass


class Div(Element):
    pass


class H1(Element):
    pass


class H2(Element):
    pass


class H3(Element):
    pass


class P(Element):
    pass


class Ul(Element):
    pass


class Li(Element):
    pass


class A(Element):
    pass


class Form(Element):
    pass


class Textarea(Element):
    pass


class Input(EmptyElement):
    pass


class Pre(Element):
    pass
