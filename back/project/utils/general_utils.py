from functools import lru_cache
import re
class GeneralUtils:
    
    def schema_to_dict(schema):
        arguments = {}
        if isinstance(schema, dict):
            arguments = schema
        else:
            arguments = schema.__dict__
        return arguments
    
    
    @staticmethod
    @lru_cache
    def load_file(file_name):
        data = None
        with open(file_name) as fh:
            data = fh.read()

        return data
    
    def is_email(email):
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(patron, email) is not None
