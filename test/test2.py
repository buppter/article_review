class Permission:
    AUTHOR = 2
    REVIEWER = 4
    EDITOR = 8
    ADMIN = 16


def insert_roles():
    roles = {
        'Author': [Permission.AUTHOR],
        'Reviewer': [Permission.REVIEWER],
        'Editor': [Permission.EDITOR],
        'Admin': [Permission.ADMIN],
    }
    default_role = 'Author'
    for r in roles:
        # role = Role.query.filter_by(name=r).first()
        # if role is None:
        #     role = Role(name=r)
        role = r
        # role.reset_permissions()
        for perm in roles[r]:
            print(perm)


def is_list():
    r = []
    if r:
        print("r is not none")
    if not r:
        print("r is none")


def test():
    list = [1, 2, 3]
    if 3 in list:
        return True
    else:
        return False


if __name__ == "__main__":
    test()
