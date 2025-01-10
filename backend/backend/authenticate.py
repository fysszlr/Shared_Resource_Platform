from user.models import Users
def user_authenticate(token):
    user = Users.objects.filter(token=token).first()
    if not user or user.block:
        return False, None
    else:
        return True, user
