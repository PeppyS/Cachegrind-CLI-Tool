import click
import git
import os
import requests

class Performance(object):

    def __init__(self):
        self.author = 'Peppy Sisay'
        self.baseURL = 'https://dev.tradesy.com';
        self.profileQueryParam = '?XDEBUG_PROFILE=1';
        print "Author is " + self.author
        return

    def triggerWebPage(self):
        page = '/bags'
        print "Triggering web page: " + page
        r = requests.get(self.baseURL + page + self.profileQueryParam)
        print r
        return

@click.group()
def cli():
    """Track performance"""
    pass

@cli.command()
def	test():
    """Test."""
    p = Performance()
    p.triggerWebPage()

if __name__ == '__main__':
    test()
