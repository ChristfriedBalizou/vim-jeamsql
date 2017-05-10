from db import Database

import argparse
import sys
import os

PATH_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(PATH_DIR, 'jeamsql.ini')

def check_config(path):
    filepath = os.path.expanduser(path)
    return os.path.exists(filepath)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--query',
            default=None,
            help='SQL query e.g: Insert, Select...'
            )
    parser.add_argument('-c', '--config',
            default=CONFIG_PATH,
            help=("Config file path containing" +
                "databases properties")
            )
    parser.add_argument('-d', '--database',
            help=("Database section fron the confiuration file")
            )
    parser.add_argument('-x', '--excetuce',
            default=False,
            action='store_true',
            dest='persist',
            help=('Execute query with no results.' +
                'Use this for Insert, Update... queries')
            )
    parser.add_argument('--list-tables',
            default=False,
            action='store_true',
            dest='list_tables',
            help='List all tables in database'
            )
    parser.add_argument('--description',
            default=False,
            action='store_true',
            dest='desc',
            help='List all tables with description in database'
            )
    parser.add_argument('-n', '--name',
            help=("Table name to view."+
                "to use with -d and --list-tables options")
            )

    parser.add_argument('--formate',
            help="Output format",
            default=None
            )

    options = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not check_config(options.config):
        print "Configuration file %s not found." % options.config
        sys.exit(1)

    if options.database is None:
        print "Option database (-d|--database) not setted."
        sys.exit(1)

    db = Database(section=options.database, config_path=options.config)

    if options.query:
        if not options.persist:
            print db.select(
                    query=options.query,
                    fmt=options.formate
                    )
        else:
            db.execute(query=options.query)

    if options.list_tables:
        print db.tables(
                name=options.name,
                fmt=options.formate
                )

    if options.desc:
        print db.description(
                table_name=options.name,
                fmt=options.formate
                )
