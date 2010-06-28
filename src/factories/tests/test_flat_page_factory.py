"""
Tests for FlatPageFactory.
"""
from django.test import TestCase
from django.contrib.flatpages.models import FlatPage
from factories.flat_pages import FlatPageFactory


class FlatPageFactoryTests(TestCase):
    """
    Tests for the FlatPageFactory class.
    """
    def setUp(self):
        self.factory = FlatPageFactory()

    def test_build_flat_page(self):
        """
        The ``build_flat_page`` method should build but not save a FlatPage
        object.
        """
        flat_page = self.factory.build_flat_page()
        self.assertTrue(isinstance(flat_page, FlatPage))
        self.assertFalse(flat_page.pk, "FlatPage is not saved.")
        self.assertEqual(flat_page.url, '/test/page/')
        self.assertEqual(flat_page.title, 'Test Page')
        self.assertEqual(flat_page.content, '<h1>Test Page</h1>')
        self.assertEqual(flat_page.registration_required, False)

    def test_create_flat_page(self):
        """
        The ``create_flat_page`` method should build and save a FlatPage
        object.
        """
        flat_page = self.factory.create_flat_page()
        self.assertTrue(isinstance(flat_page, FlatPage))
        self.assertTrue(flat_page.pk, "FlatPage is saved.")
        self.assertEqual(flat_page.url, '/test/page/')
        self.assertEqual(flat_page.title, 'Test Page')
        self.assertEqual(flat_page.content, '<h1>Test Page</h1>')
        self.assertEqual(flat_page.registration_required, False)

    def test_argument_overrides(self):
        """
        The user should be able to override the default values of the
        blueprint.
        """
        flat_page = self.factory.build_flat_page(title='My Title',
            content='Content')
        self.assertEqual(flat_page.url, '/test/page/')
        self.assertEqual(flat_page.title, 'My Title')
        self.assertEqual(flat_page.content, 'Content')

    def test_interpolation(self):
        """
        An interpolated value specified in the blueprint should change as the
        values it references are overridden.
        """
        flat_page = self.factory.build_flat_page(title='My Title')
        self.assertEqual(flat_page.title, 'My Title')
        self.assertEqual(flat_page.content, '<h1>My Title</h1>')

    def test_protected_flat_page(self):
        """
        The protected_flat_page blueprint should create a FlatPage that
        requires registration.
        """
        flat_page = self.factory.build_protected_flat_page()
        self.assertTrue(isinstance(flat_page, FlatPage))
        self.assertFalse(flat_page.pk, "FlatPage is not saved.")
        self.assertEqual(flat_page.url, '/test/page/')
        self.assertEqual(flat_page.title, 'Test Page')
        self.assertEqual(flat_page.content, '<h1>Test Page</h1>')
        self.assertEqual(flat_page.registration_required, True)
