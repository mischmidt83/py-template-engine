__doc__ = f"""
Usage:
  {__file__} [--count=N] PATH FILE...

Arguments:
  FILE     input file
  PATH     out directory

Options:
  --count=N   number of operations

"""
import os

# Check that requirements ar installed

script_path = os.path.dirname(os.path.realpath(__file__))

try:
    from docopt import docopt
except ImportError:
    exit(f"""{__file__} requires that `docopt` library (https://github.com/docopt/docopt)"""
         f""" is installed: \n    pip install -r {script_path}\\requirements.txt""")

try:
    from schema import Schema, And, Or, Use, SchemaError
except ImportError:
     exit(f"""{__file__} requires that `schema` data-validation library (https://github.com/halst/schema)"""
         f""" is installed: \n    pip install -r {script_path}\\requirements.txt""")

# main

if __name__ == '__main__':
    args = docopt(__doc__)

    schema = Schema({
        'FILE': [Use(open, error='FILE should be readable')],
        'PATH': And(os.path.exists, error='PATH should exist'),
        '--count': Or(None, And(Use(int), lambda n: 0 < n < 5),
                      error='--count=N should be integer 0 < N < 5')})
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    print(args)