import logging

import re
import typing
from typing import List
from pathlib import Path

from jinja2 import Markup
from markdown import markdown

from ._type_hint_helpers import PathString


class Page:
    """Base component used to make web pages.

    All components that represent
    content in HTML, XML, or JSON generated by Render Engine should be a Page
    object.

    Pages can be rendered directly from a template or from a file.

    Page objects can be used to extend existing page objects.

    Examples
    --------
    # Basic Page with No Template Variables
    @site.register_route('basic_page.html')
    class BasicPage(Page):
        template = 'template_file.html' # user provided template

    # Basic Page with Variables
    @site.register_route('page_with_vars')
    class PageWithVars(Page):
        title = 'Site Title'

    # Page Loading from File
    @site.register_route('page_from_file')
    class PageFromFile(Page):
        content_path = 'index.md' # loaded from content path can be '.md' or '.html'


    # Page Inherited from Other Page
    @site.register_route('basic_page.html')
    class BasicPage(Page):
        template = 'template_file.html' # user provided template
        title = 'Base Page'

    @site.register_route('other_page.html')
    class InheritingPage(Page):
        # template will be inherited from the BasicPage
        title = 'Inherited Page'

    Attributes
    ----------
    engine: str
        The engine that the Site should refer to or the site's default engine
    template: str
        The template that the Site should refer to. If empty, use site's default
    match_param: str 
        The regular expression used to identify metadata in a content file
        (default "r(^\w+: \b.+$)")
    routes: List[str]
        all routes that the file should be created at. default []
    content_path: List[PathString], optional
        the filepath to load content from.

    Methods
    -------
    """

    engine: str = ""
    template: str = ""
    match_param: str = r"(^\w+: \b.+$)"
    routes: List[str] = []

    def __init__(self, content_path=None):
        """If a content_path exists, check the associated file, processing the
        vars at the top and restitching the remaining lines
        """

        if content_path:
            if not Path(content_path).exists():
                raise ValueError("The content_path does not exist")

            content = Path(content_path).read_text()
            self.content_path = content_path
            parsed_content = re.split(self.match_param, content, flags=re.M)
            self._content = parsed_content.pop().strip()
            valid_attrs = [x for x in parsed_content if x.strip("\n")]
            # We want to allow leading spaces and tabs so only strip new-lines

            for attr in valid_attrs:
                name, value = attr.split(": ", maxsplit=1)
                setattr(self, name.lower(), value.strip())

            if not hasattr(self, "slug"):
                if hasattr(self, "title"):
                    self.slug = self.title.lower().replace(" ", "_")
                else:
                    self.slug = self.__class__.__name__.lower().replace(" ", "_")

            else:
                self.slug = self.slug.lower().replace(" ", "_")

    @property
    def html(self):
        """the text from self._content converted to html"""

    def __str__(self):
        return self.slug

    @property
    def html(self):
        """the text from self._content converted to html"""

        if hasattr(self, "_content"):
            return markdown(self._content)

        else:
            return ""

    @property
    def content(self):
        """html = rendered html (not marked up). Is None if content is none"""
        return Markup(self.html)
