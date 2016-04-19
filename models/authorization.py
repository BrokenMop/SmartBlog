# -*- coding: utf-8 -*-
def user_belongs_group(user, group):
    if group.role == ADMIN_GROUP or group.role == AUTUOR_GROUP or group.role == VISITOR_GROUP:
            query = (db.auth_membership.user_id == user and db.auth_membership.group_id == group)
            results= db(query).select()
            return results != 0
    else:
        return False
