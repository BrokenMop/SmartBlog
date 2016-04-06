# -*- coding: utf-8 -*-

import string
import random
from random import randint
import datetime

ADMIN_GROUP = 'admin'
AUTUOR_GROUP = 'author'
VISITOR_GROUP = 'visitor'

TEST_UNICODE_RANGE = range(0x4E00, 0x9fa5)
TEST_ASCII_STRING = string.lowercase + string.ascii_uppercase + string.digits + string.punctuation

def get_random_ustring(min_len, max_len):
    return ''.join(unichr(random.choice(TEST_UNICODE_RANGE)) for _ in range(randint(min_len, max_len)))

def get_random_string(min_len, max_len):
    return ''.join(random.choice(TEST_ASCII_STRING) for _ in range(randint(min_len, max_len)))

def populate_user(username, email, password):
    user = db.auth_user.insert(username = username, email =email, password = CRYPT()(password)[0])
    db.commit()
    return user

def assign_group(user, group):
    membership = db.auth_membership.insert(user_id = user, group_id = group)
    db.commit()
    return membership

def populate_category():
    #NEED TO CONSIDER TRANSLATION
    category_list = []
    category_list.append(db.category.insert(category_name = '测评'))
    category_list.append(db.category.insert(category_name = '新闻'))
    category_list.append(db.category.insert(category_name = '停产'))
    db.commit()
    return category_list

def populate_post(category_list, num_of_posts, author):
    post_list = []
    for i in range(num_of_posts):
        if bool(random.getrandbits(1)):
            title = get_random_string(10, 30)
            body = get_random_string(50, 400)
        else:
            title = get_random_ustring(10, 20)
            body = get_random_ustring(40, 350)
        new_post = db.post.insert(title = title,
                               body = body,
                               category = category_list[i % len(category_list)],
                               post_datetime = datetime.datetime.now(),
                               author = author,
                               if_display_author = bool(random.getrandbits(1)))
        post_list.append(new_post)
        db.commit()
    return new_post

def init_db():
    if db(db.auth_user).isempty() and db(db.auth_group).isempty():
        admin = populate_user('admin1', 'jerryliu0228@gmail.com', 'password')
        admin_group = db.auth_group.insert(role = ADMIN_GROUP)
        author_group = db.auth_group.insert(role = AUTUOR_GROUP)
        visitor_group = db.auth_group.insert(role = VISITOR_GROUP)
        assign_group(admin, admin_group)
        category_list = populate_category()
        populate_post(category_list, 20, admin)



def clean_db():
    db(db.auth_membership.id >0).delete()
    db(db.auth_user.id >0).delete()
    db(db.auth_group.id >0).delete()
    db(db.post.id >0).delete()
    db(db.category.id >0).delete()
    db.commit()

#clean_db()
#init_db()
