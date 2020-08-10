def change_role(username, *new_roles):
    from coderg.extensions import db
    from coderg.models import Role, User
    from config.config import params
    from .verify import check_role

    if check_role('ADMIN'):
        roles_avl = params['roles']
        user = User.query.filter_by(username=username).first()

        for role in roles_avl:
            # new role added
            if role in new_roles and role not in user.role:
                db.session.add(Role(title=role, username=username))

            # role removed
            elif role not in new_roles and role in user.role:
                for role_obj in user._user_role:
                    if role_obj.title == role:
                        db.session.delete(role_obj)

        db.session.commit()
