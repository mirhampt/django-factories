from setuptools import setup, find_packages

setup(
    name = "django-factories",
    version = "0.1",
    url = "",
    license = "MIT",
    description = "A model factory for Django apps.",
    author = "Michael Hampton",
    packages = find_packages("src"),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
