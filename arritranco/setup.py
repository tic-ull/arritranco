from setuptools import setup
# This setup.py is intended to install the individuals apps, for use in others projects
# At this time it just install location app

setup(
    name = "Arritranco",
    version = "0.1",
    packages = ["location", "hardware", "things",],
    author = "STIC-ULL",
    author_mail = "sistemas@ull.es",
    description = "This is an inventory tool for IT resource",
    license = "AGPL",
    keywords = "inventory, stock"
)
