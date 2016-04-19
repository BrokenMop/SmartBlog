# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from test.py")

class TestCase:
    def __init__(self, number, result):
         self.number = number
         self.result = result

def runAll():
    cases = []
    cases.append(TestCase('case001', case001()))
    cases.append(TestCase('case002', case002()))
    return dict(cases = cases)

def case001():
    group= populate_group(ADMIN_GROUP)
    user = populate_user('test_user_from_case_001', 'test_user_from_case_001@test.com', 'test_user_from_case_001')
    assign_group(user, group)
    result = user_belongs_group(user, group)
    db(db.auth_membership.user_id == user and db.auth_membership.group_id == group).delete()
    db(db.auth_user.id == user).delete()
    db(db.auth_group.id == group).delete()
    db.commit()
    if result:
        return 'PASS'
    else:
        return 'FAIL'


def case002():
    test_theme_name = 'test_theme_from_case002'
    result = False
    result = (count_theme() == 0)
    insert_new_theme(test_theme_name)
    result = result and (count_theme() == 1)
    insert_new_theme(test_theme_name)
    result = result and (count_theme() == 1)
    result = result and (search_theme(test_theme_name) is not None)
    result = result and if_theme_exists(test_theme_name)
    delete_theme(test_theme_name)
    result = result and (count_theme() == 0)
    if result:
        return 'PASS'
    else:
        return 'FAIL'
    
def visualize():
    return getAllSubthemeWithCount()
