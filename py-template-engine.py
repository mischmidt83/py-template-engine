__doc__ = f"""
Usage:
  {__file__} TEMPLATE_FILE CONFIG_FILE

Arguments:
  CONFIG_FILE     input file
  TEMPLATE_FILE     template file

"""
import os
import configparser

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

    config = configparser.ConfigParser(
    defaults={'index':0,
              'port_offset':10,
              'timezone':'timezone',
              'db_name':'infinity_db',
              'db_user':'infinity_user',
              'db_password':'infinity_pw'
              })

    try:
        config.read(args['CONFIG_FILE'])
    except Exception as e :
        print(str(e))

    try:
        # general
        index = config.get('general', 'index')
        port_offset = config.get('general', 'port_offset')
        timezone = config.get('general', 'timezone')

        # database
        db_name = config.get('database', 'db_name')
        db_user = config.get('database', 'db_user')
        db_password = config.get('database', 'db_password')

    except Exception as e :
        print(str(e),' could not read configuration file')

    print(index, port_offset, timezone, db_name, db_user, db_password)

    # pass directory containing the templates

    # file_loader = FileSystemLoader('templates')
    # env = Environment(loader=file_loader)

    # load the template
    # template = env.get_template(args['TEMPLATE_FILE'])

    with open(args['TEMPLATE_FILE']) as file_:
      template = Template(file_.read())

      output = template.render(db_name=db_name)
      print(output)


    print(args)