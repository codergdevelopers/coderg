def change_role(username, *new_roles):
    """
    :param username: username of user
    :param new_roles: new roles to be given to the user including any previous roles
    =>If a previous role is not present in new_roles then it will be removed

    :return:boolean
    """
    from coderg.extensions import db
    from coderg.models import Role, User
    from config.config import params
    from .verify import check_role

    if check_role('ADMIN'):
        roles_avl = params['roles']
        user = User.query.filter_by(username=username).first()

        for role in roles_avl:
            # add new role
            if role in new_roles and role not in user.role:
                db.session.add(Role(title=role, username=username))

            # remove role
            elif role not in new_roles and role in user.role:
                for role_obj in user._user_role:
                    if role_obj.title == role:
                        db.session.delete(role_obj)

        db.session.commit()
