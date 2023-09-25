from util import *

names_from_primary_info = get_values_alchemy('primary_info', ['name','created_by'])

print(names_from_primary_info)