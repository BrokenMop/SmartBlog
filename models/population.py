# -*- coding: utf-8 -*-

import string
import random
from random import randint
import datetime

# ================ TEST DATABASE ==========
ADMIN_GROUP = 'admin'
AUTUOR_GROUP = 'author'
VISITOR_GROUP = 'visitor'

THEME_TO_SUBTHEME = {'Creator' : ['Three in One', 'Modular Buildings'],
          'City' : ['Fire', 'Police', 'Arctic', 'Volcano'],
          'Friends' : ['Pop Star', 'Heartlake City'],
          'Ideas' : [],
          'Super Heroes' : ['DC Comics', 'Marvel']}

# add atrribute ANIMALFIG
LEGO_SET = [['10251', 'Brick Bank', 2380, 5, 2016, 169.99, 149.99, 119.99, '16+', 'Creator', 'Modular Buildings'],
            ['60107', 'Fire Ladder Truck', 214, 2, 2016, None, None, None, '5-12', 'City', 'Fire'],
            ['60117', 'Van&Caravan', None, 2, 2016, 19.99, 19.99, 17.99, '5-12', 'City', DEFAULT_SUBTHEME_NAME],
            ['41122', 'Adventure Camp Tree House', 726, 3, 2016, None, None, None, '7-12', 'Friends', 'Adventure Camp'],
            ['41126', 'Hearlake Riding Club', 575, 2, 2016, None, None, None, '6-12', 'Friends', 'Heartlake'],
            ['21305', 'Maze', 769, 0, 2016, None, None, None, '10+', 'Ideas', DEFAULT_SUBTHEME_NAME]]

TEST_UNICODE_RANGE = range(0x4E00, 0x9fa5)
TEST_ASCII_STRING = string.lowercase + string.ascii_uppercase + string.digits + string.punctuation

def get_random_ustring(min_len, max_len):
    return ''.join(unichr(random.choice(TEST_UNICODE_RANGE)) for _ in range(randint(min_len, max_len)))

def get_random_string(min_len, max_len):
    return ''.join(random.choice(TEST_ASCII_STRING) for _ in range(randint(min_len, max_len)))

# ================== POPULATION FUNCS ================

def populate_user(username, email, password):
    user = db.auth_user.insert(username = username, email =email, password = CRYPT()(password)[0])
    db.commit()
    return user

def populate_group(group_name):
    group = db.auth_group.insert(role = group_name)
    db.commit()
    return group

def assign_group(user, group):
    membership = db.auth_membership.insert(user_id = user, group_id = group)
    db.commit()
    return membership

def populate_post_category():
    #NEED TO CONSIDER TRANSLATION
    category_list = []
    category_list.append(db.post_category.insert(category_name = 'Category6'))
    category_list.append(db.post_category.insert(category_name = 'Category5'))
    category_list.append(db.post_category.insert(category_name = 'Category4'))
    db.commit()
    return category_list

def populate_post_tag():
    tag_list = []
    tag_list.append(db.post_tag.insert(tag_name = 'Tag1'))
    tag_list.append(db.post_tag.insert(tag_name = 'Tag2'))
    tag_list.append(db.post_tag.insert(tag_name = 'Tag3'))
    tag_list.append(db.post_tag.insert(tag_name = 'Tag4'))
    tag_list.append(db.post_tag.insert(tag_name = 'Tag5'))
    db.commit
    return tag_list

def populate_post(category_list, tag_list, num_of_posts, author):
    post_list = []
    for i in range(num_of_posts):
        # ASCII POST
        if bool(random.getrandbits(1)):
            title = get_random_string(10, 30)
            body = get_random_string(50, 400)
        # UNICODE POST
        else:
            title = get_random_ustring(10, 20)
            body = get_random_ustring(40, 350)
        # INSERT NEW POST
        new_post = db.post.insert(title = title,
                               body = body,
                               category = category_list[i % len(category_list)],
                               post_datetime = datetime.datetime.now(),
                               author = author,
                               if_display_author = bool(random.getrandbits(1)))
        # GET RANDOM TAGS (0, ALL)
        selected_tags = random.sample(tag_list, randint(0,len(tag_list)))
        # IF TAG LIST IS NOT EMPTY
        if selected_tags:
            for tag in selected_tags:
               db.post_tag_rel.insert(post = new_post, tag = tag)
        post_list.append(new_post)
        db.commit()
    return new_post

def populate_theme(theme_list):
    for theme in theme_list:
        get_or_insert_theme(theme)

def populate_subtheme(theme_subtheme_dict):
    for theme, subtheme_list in theme_subtheme_dict.iteritems():
        if subtheme_list:
            for subtheme in subtheme_list:
                get_or_insert_subtheme(subtheme, theme)

def populate_lego_set(set_info_lists):
    for set_info_list in set_info_lists:
         insert_new_set_from_strlist(*set_info_list)

def insert_new_set_from_strlist(set_number, set_name, piece_count, minifig_count, year_released,
                   rrp_usd, rrp_euro, rrp_pound, age_range,
                   theme_name, subtheme_name):

    theme = get_or_insert_theme(theme_name.strip())
    subtheme = get_or_insert_subtheme(subtheme_name.strip(), theme.theme_name)
    age_range = get_or_insert_age_range(age_range.strip())

    return insert_set(set_number, set_name, piece_count, minifig_count, year_released,
                   rrp_usd, rrp_euro, rrp_pound, age_range,
                   theme, subtheme)


# ================== CLEAN FUNCS ================

def clean_db():
    clean_post_tables()
    clean_user_tables()
    clean_set_tables()

def clean_user_tables():
    db.auth_membership.truncate()
    db.auth_group.truncate()
    db.auth_user.truncate()
    db.commit()

def clean_post_tables():
    db.post_tag_rel.truncate()
    db.post_tag.truncate()
    db.post.truncate()
    db.post_category.truncate()
    db.commit()

def clean_set_tables():
    db.lego_set.truncate()
    db.subtheme.truncate()
    db.theme.truncate()
    db.age_range.truncate()
    db.commit()


def init_db():
    if db(db.auth_user).isempty() and db(db.auth_group).isempty():
        # users and groups
        admin = populate_user('administrator', 'jerryliu0228@gmail.com', 'pass')
        admin_group = populate_group(ADMIN_GROUP)
        author_group = populate_group(AUTUOR_GROUP)
        visitor_group = populate_group(VISITOR_GROUP)
        assign_group(admin, admin_group)

        # categories, tags, and posts
        category_list = populate_post_category()
        tag_list = populate_post_tag()
        populate_post(category_list, tag_list, 20, admin)

        # lego sets
        populate_theme(list(THEME_TO_SUBTHEME.keys()))
        populate_subtheme(THEME_TO_SUBTHEME)
        populate_lego_set(LEGO_SET)

clean_db()
init_db()
