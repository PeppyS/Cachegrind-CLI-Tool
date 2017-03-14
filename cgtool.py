import re
import click
import os
import glob

# Tool for parsing/clearing cachegrind outputs
class CachegrindTool(object):
    def __init__(self, path):
        # Where cache grind outputs are located
        self.cachegrindOutputDir = path
        # File name of cacheGrind outputs
        self.cachegrindFileName = 'cachegrind';
        self.cachegrindPattern = '*.out.*';
        return

    def parse(self):
        # Initialize group stats
        statsGrouped = dict()
        statsGrouped[CachegrindStats.HOME_PAGE] = []
        statsGrouped[CachegrindStats.CATEGORY_PAGE] = []
        statsGrouped[CachegrindStats.IDP_PAGE] = []

        # Locate cachegrind outputs, and begin parsing
        for filename in glob.glob(os.path.join(self.cachegrindOutputDir, self.cachegrindPattern)) :
            with open(filename) as cachegrindFile:
                stats = CachegrindStats()
                for line in cachegrindFile:
                    # Total response time is prefixed with text 'summary:'
                    if 'summary:' in line:
                        # Parse total response time out of line
                        stats.totalLoadTime = int(re.search(r'\d+', line).group()) / 1000
                    if 'SiteController->actionIndex' in line:
                        stats.type = CachegrindStats.HOME_PAGE
                    elif 'CategoryController->actionIndex' in line:
                        stats.type = CachegrindStats.CATEGORY_PAGE
                    elif 'ItemController->actionIdp' in line:
                        stats.type = CachegrindStats.IDP_PAGE

                # Only add to list if we were able to identify this page
                if stats.type:
                    statsGrouped[stats.type].append(stats)

        # Ensure stats were collected
        if not any(statsGrouped.values()):
            print("No cachegrind files were found in path: " + self.cachegrindOutputDir)
        else:
            # Build averages and print back
            for pageType, group in statsGrouped.items():
                if len(group):
                    averageTotal = int(sum(stats.totalLoadTime for stats in group) / len(group))
                    print(pageType)
                    print("Number of cachegrinds parsed: " + str(len(group)))
                    print("Average load time: " + str(averageTotal) + "\n")
        return

    def clear(self):
        count = 0
        # Locate and remove cachegrind outputs
        for filename in glob.glob(os.path.join(self.cachegrindOutputDir, self.cachegrindPattern)) :
            count += 1
            os.remove(filename)
        if count:
            print("Removed " + str(count) + " cachegrind files")
        else:
            print("No cachegrind files were found in path: " + self.cachegrindOutputDir)
        return

# Encapsulates data collected from cachegrind output
class CachegrindStats(object):
    # Page types
    HOME_PAGE = 'Home Page'
    CATEGORY_PAGE = 'Category Page'
    IDP_PAGE = 'IDP Page'

    # Data collected per cachegrind output
    type = ''
    totalLoadTime = 0.0

@click.group()
def cli():
    """Get load time from generated cachegrind outputs"""
    pass

@cli.command()
@click.option('--path')
def	parse(path):
    """Parses cache grind output files, and generates average response times for Home/Category/IDP Pages"""
    CachegrindTool(path).parse()

@cli.command()
@click.option('--path')
def clear(path):
    """Clears all cache grind output files"""
    CachegrindTool(path).clear()

if __name__ == '__main__':
    cli()
