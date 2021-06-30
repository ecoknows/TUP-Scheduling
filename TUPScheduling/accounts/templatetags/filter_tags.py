

from django.template import Library

register = Library()

@register.simple_tag
def get_starting_tile(parent_tile, tile):
   #do your stuff
   return ((parent_tile - 1) * 6) +  tile - 1