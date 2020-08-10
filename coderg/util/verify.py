def check_role(*args):
    """
    :param args:('ADMIN','EDITOR',['CHIEF','HEAD'])
            user should have all roles and any one from list
    =>user should be 'ADMIN' and 'EDITOR' and ('CHIEF' or 'HEAD')

    :return:boolean
    """
    from flask import session
    from coderg.models import User

    if 'user' not in session:
        return False
    else:
        user_role = User.query.filter_by(username=session['user']).first().role

        for role in args:

            if type(role) == list:
                for or_role in role:
                    if or_role in user_role:
                        break
                else:
                    return False

            elif role not in user_role:
                return False

        return True


def role_required(*args, redirect_to='/'):
    def inner(func):
        def wrapper():
            from flask import redirect

            if check_role(args):
                func()
            else:
                return redirect(redirect_to)

        return wrapper

    return inner
