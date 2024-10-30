from django import template
from core.models import User

# To use the displayname filter in a template include
# {% load app_tags %}

register = template.Library()

@register.filter(name='displayname')
def display_name(username):

    try:
        # Attempt to get the user from the database
        user = User.objects.get(username=username)

        # prepare name part if they exist
        name_parts = []

        if user.prefix:       name_parts.append(user.prefix)
        if user.first_name:   name_parts.append(user.first_name)
        if user.middle_name:  name_parts.append(user.middle_name)
        if user.last_name:    name_parts.append(user.last_name)

        # If any name part exists, join them into a readable name
        if name_parts:
            return " ".join(name_parts)
        else:
            # If no detailed name is available, fall back to the username (ID)
            return user.username
    except User.DoesNotExist:

        # If the user is not found in the database, return "Unknown User"
        return "Unknown User"
        