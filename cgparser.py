import re

# Parser for cachegrind output files
class CachegrindParser(object):
    def __init__(self, cachegrindOutput):
        self.cachegrindOutput = cachegrindOutput
        return

    # Parses & returns stats for given output
    def parse(self):
        stats = CachegrindStats()
        for line in self.cachegrindOutput:
            # Total response time is prefixed with text 'summary:'
            if 'summary:' in line:
                # Parse total response time out of line
                stats.totalLoadTime = int(re.search(r'\d+', line).group()) / 1000
            elif 'SiteController->actionIndex' in line:
                stats.type = CachegrindStats.HOME_PAGE
            elif 'CategoryController->actionIndex' in line:
                stats.type = CachegrindStats.CATEGORY_PAGE
            elif 'ItemController->actionIdp' in line:
                stats.type = CachegrindStats.IDP_PAGE
        return stats

# Encapsulates data collected from cachegrind output
class CachegrindStats(object):
    # Page types
    HOME_PAGE = 'Home Page'
    CATEGORY_PAGE = 'Category Page'
    IDP_PAGE = 'IDP Page'

    # Data collected per cachegrind output
    type = ''
    totalLoadTime = 0.0
