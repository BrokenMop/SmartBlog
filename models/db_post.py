# -*- coding: utf-8 -*-

db.define_table('category',
                Field('category_name'))

db.define_table('post',
                Field('title'),
                Field('body', 'text'),
                Field('category', 'reference category'),
                Field('author', 'reference auth_user'),
                Field('if_display_author', 'boolean'),
                Field('post_datetime', 'datetime')
                )

def getAllCategories():
    query = db.category.id>0
    rows= db(query).select()
    return rows

def getAllCategoriesWithCount():
    count = db.post.id.count().with_alias('count')
    rows=db().select(db.category.category_name, db.category.id, count,
        left=db.post.on(db.category.id==db.post.category), groupby = db.category.id)
    return rows
