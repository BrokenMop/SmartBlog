# -*- coding: utf-8 -*-
PRICE_PER_PIECE_FORMAT = "{0:.2f}"
DEFAULT_SUBTHEME_NAME = "Default"

db.define_table('theme',
                Field('theme_name'))

db.define_table('subtheme',
                Field('subtheme_name'),
                Field('theme', 'reference theme')
                )

db.define_table('age_range',
                Field('age_start', 'integer',
                      compute = lambda r : calculate_age_range(r['age_range'])[0]),
                Field('age_end', 'integer',
                      compute = lambda r : calculate_age_range(r['age_range'])[1]),
                Field('age_range')
                )

db.define_table('lego_set',
                Field('set_number'),
                Field('set_name'),
                Field('piece_count', 'integer'),
                Field('minifig_count', 'integer'),
                Field('year_released', 'integer'),
                Field('rrp_usd', 'double'),
                Field('rrp_euro', 'double'),
                Field('rrp_pound', 'double'),
                Field('ppp_usd', 'double',
                      compute = lambda r : calculate_price_per_piece(r['rrp_usd'], r['piece_count'])),
                Field('ppp_euro', 'double',
                      compute = lambda r : calculate_price_per_piece(r['rrp_euro'], r['piece_count'])),
                Field('ppp_pound', 'double',
                      compute = lambda r : calculate_price_per_piece(r['rrp_pound'], r['piece_count'])),
                Field('age_range', 'reference age_range'),
                Field('theme', 'reference theme'),
                Field('subtheme', 'reference subtheme'),
                Field('main_photo')
                )

# TRIGGER ================================================================================
def calculate_price_per_piece(price, piece):
    if price is not None and piece is not None and piece != 0:
        return float(PRICE_PER_PIECE_FORMAT.format(float(price) * 100 / piece))
    else:
        return None

def calculate_age_range(age_range):
    if '-' in age_range:
        sub = age_range.split('-')
        return (int(sub[0]), int(sub[1]))
    elif '+' in age_range:
        sub = age_range.split('+')
        return (int(sub[0]), 100)
    else:
        return (0, 100)

# SELECT ================================================================================
def getAllTheme():
    query = db.theme.id>0
    rows = db(query).select()
    return rows

def getAllSubtheme():
    query = db.subtheme.id>0
    rows = db(query).select()
    return rows

def getAllAgeRange():
    query = db.age_range.id>0
    rows = db(query).select()
    return rows



# COUNTER ================================================================================
def getAllThemeWithCount():
    count = db.lego_set.id.count().with_alias('count')
    rows=db().select(db.theme.theme_name, db.theme.id, count,
        left=db.lego_set.on(db.theme.id == db.lego_set.theme), 
        groupby = db.theme.id, orderby = db.theme.theme_name)
    return rows


def getAllSubthemeWithCount():
    count = db.lego_set.id.count().with_alias('count')
    rows=db().select(db.subtheme.subtheme_name, db.subtheme.id, db.subtheme.theme, db.theme.theme_name, count,
        left=[db.lego_set.on(db.subtheme.id == db.lego_set.subtheme), db.theme.on(db.subtheme.theme == db.theme.id)], 
        groupby = db.subtheme.id, orderby = db.theme.theme_name | db.subtheme.subtheme_name)
    return rows

def getAllAgeRangeWithCount():
    count = db.lego_set.id.count().with_alias('count')
    rows=db().select(db.age_range.age_range, db.age_range.id, count,
        left=db.lego_set.on(db.age_range.id == db.lego_set.age_range),
        groupby = db.age_range.id, orderby = db.age_range.age_start | db.age_range.age_end)
    return rows


# SEARCH ================================================================================
def search_theme(theme_name):
    return db(db.theme.theme_name == theme_name).select().first()

def search_subtheme(subtheme_name, theme_name):
    theme = search_theme(theme_name)
    if theme:
        return db((db.subtheme.subtheme_name == subtheme_name) & (db.subtheme.theme == theme)).select().first()
    else:
        return None

def search_age_range(age_range_str):
    return db(db.age_range.age_range == age_range_str).select().first()




# EXIST ================================================================================
def if_theme_exists(theme_name):
    return search_theme(theme_name) is not None

def if_subtheme_exists(subtheme_name, theme_name):
    return search_subtheme(subtheme_name, theme_name) is not None

def if_age_range_exists(age_range_str):
    return search_age_range(age_range_str) is not None



# COUNT ================================================================================
def count_theme():
    return db(db.theme.id > 0).count()



# INSERT ================================================================================
def get_or_insert_theme(theme_name):
    if not if_theme_exists(theme_name):
        theme = db.theme.insert(theme_name = theme_name)
        subtheme = db.subtheme.insert(subtheme_name = DEFAULT_SUBTHEME_NAME, theme = theme)
        db.commit()
        return theme
    else:
        return search_theme(theme_name)

def get_or_insert_subtheme(subtheme_name, theme_name):
    if not if_subtheme_exists(subtheme_name, theme_name):
        if if_theme_exists(theme_name):
            theme = search_theme(theme_name)
        else:
            theme = insert_new_theme(theme_name)
        subtheme = db.subtheme.insert(subtheme_name = subtheme_name, theme = theme)
        db.commit()
        return subtheme
    else:
        return search_subtheme(subtheme_name, theme_name)

def get_or_insert_age_range(age_range_str):
    if not if_age_range_exists(age_range_str):
         age_range = db.age_range.insert(age_range = age_range_str)
         db.commit()
         return age_range
    else:
        return search_age_range(age_range_str)

def insert_set(set_number, set_name, piece_count, minifig_count, year_released,
                   rrp_usd, rrp_euro, rrp_pound, age_range,
                   theme, subtheme):
    lego_set = db.lego_set.update_or_insert(set_number = set_number,
                                       set_name = set_name.strip(),
                                       piece_count = piece_count,
                                       minifig_count = minifig_count,
                                       year_released = year_released,
                                       rrp_usd = rrp_usd,
                                       rrp_euro = rrp_euro,
                                       rrp_pound = rrp_pound,
                                       age_range = age_range,
                                       theme = theme,
                                       subtheme = subtheme)
    db.commit()
    return lego_set

# DELETE ==========
def delete_theme(theme_name):
    db(db.theme.theme_name==theme_name).delete();
    db.commit()
