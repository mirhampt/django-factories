"""
Factory for flatpages app.
"""
from factories import Factory, blueprint


class FlatPageFactory(Factory):
    """
    A model factory for the ``contrib.flatpages`` app.
    """
    @blueprint(model='flatpages.FlatPage')
    def flat_page(self):
        "A basic FlatPage--public, no comments."
        return {
            'url': '/test/page/',
            'title': 'Test Page',
            'content': '<h1>%(title)s</h1>',
            'enable_comments': False,
            'registration_required': False,
        }

    @blueprint(model='flatpages.FlatPage')
    def protected_flat_page(self):
        "A FlatPage that is only accessible by registered users."
        flat_page = self.flat_page()
        flat_page['registration_required'] = True
        return flat_page
