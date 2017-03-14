import click
import os
import glob
from cgparser import CachegrindParser, CachegrindStats

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
                stats = CachegrindParser(cachegrindFile).parse()
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
                    click.echo(pageType)
                    click.echo("Number of cachegrinds parsed: " + str(len(group)))
                    click.echo("Average load time: " + str(averageTotal) + "\n")
        return

    def clear(self):
        count = 0
        # Locate and remove cachegrind outputs
        for filename in glob.glob(os.path.join(self.cachegrindOutputDir, self.cachegrindPattern)) :
            count += 1
            os.remove(filename)
        if count:
            click.echo("Removed " + str(count) + " cachegrind files")
        else:
            click.echo("No cachegrind files were found in path: " + self.cachegrindOutputDir)
        return

@click.group()
def cli():
    """Get load time from generated cachegrind outputs"""
    pass

@cli.command()
@click.option('--path', default='/Users/peppytradesy/projects/tradesy-core/labs/performance/')
def	parse(path):
    """Parses cache grind output files, and generates average response times for Home/Category/IDP Pages"""
    CachegrindTool(path).parse()

@cli.command()
@click.option('--path', default='/Users/peppytradesy/projects/tradesy-core/labs/performance/')
def clear(path):
    """Clears all cache grind output files"""
    CachegrindTool(path).clear()

@cli.command()
def how():
    """Instructions on setting up this tool"""
    click.echo('Locate your php.ini configuration and make sure these values are set\n')
    click.echo('# [xdebug]')
    click.echo('xdebug.profiler_enable_trigger=1')
    click.echo('xdebug.profiler_enable=0')
    click.echo('# You can rename this folder, make sure there is a symlink to a local folder')
    click.echo('xdebug.profiler_output_dir="/performance"')
    click.echo('xdebug.profiler_output_name="cachegrind.out.%u"\n')
    click.echo('And run this: sudo apachectl -k graceful\n')
    click.echo('Now you can generate cachegrind output files by loading web pages with XDEBUG_PROFILE=1 set (GET/POST/COOKIE)')
    return

if __name__ == '__main__':
    cli()
