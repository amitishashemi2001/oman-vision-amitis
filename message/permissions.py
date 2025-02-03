from django.http import HttpResponseForbidden
import sys
def check_user_is_record_owner(user, obj):
    if user.id != obj.user.id:
        return HttpResponseForbidden('You are not allowed to modify this record')
    return None
