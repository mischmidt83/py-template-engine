__doc__ = f"""
Usage:
  {__file__} TEMPLATE_FILE CONFIG_FILE

Arguments:
  CONFIG_FILE     input file
  TEMPLATE_FILE     template file

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

try:
    from jinja2 import Template
except ImportError:
     exit(f"""{__file__} requires that `jinja2` library (https://palletsprojects.com/p/jinja/)"""
         f""" is installed: \n    pip install -r {script_path}\\requirements.txt""")

import yaml

# main

if __name__ == '__main__':
    args = docopt(__doc__)

    schema = Schema({
        # 'CONFIG_FILE': And(os.path.exists, error='CONFIG_FILE should exist'),
        'CONFIG_FILE': And(os.path.isfile, error='CONFIG_FILE should be a file'),
        # 'TEMPLATE_FILE': And(os.path.exists, error='TEMPLATE_FILE should exist'),
        'TEMPLATE_FILE': And(os.path.isfile, error='TEMPLATE_FILE should be a file')
        # '--count': Or(None, And(Use(int), lambda n: 0 < n < 5),
        #               error='--count=N should be integer 0 < N < 5'
      })
    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    # read yaml configuration
    with open(args['CONFIG_FILE']) as f:
      
        config = yaml.load(f, Loader=yaml.FullLoader)

    # read template file and render it with data
    with open(args['TEMPLATE_FILE']) as file_:
        template = Template(file_.read())

        output = template.render(config=config)
        print(output)