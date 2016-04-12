# -*- coding: utf-8 -*-


db.define_table('post_category',
                Field('category_name'))

db.define_table('post_tag',
                Field('tag_name'))

db.define_table('post',
                Field('title'),
                Field('body', 'text'),
                Field('category', 'reference post_category'),
                Field('author', 'reference auth_user'),
                Field('if_display_author', 'boolean'),
                Field('post_datetime', 'datetime')
                )

db.define_table('post_tag_rel',
                Field('post', 'reference post'),
                Field('tag', 'reference post_tag')
               )

def getAllPostCategories():
    query = db.post_category.id>0
    rows = db(query).select()
    return rows

def getAllPostCategoriesWithCount():
    count = db.post_category.id.count().with_alias('count')
    rows=db().select(db.category.category_name, db.category.id, count,
        left=db.post.on(db.post_category.id == db.post.category), groupby = db.post_category.id)
    return rows

def saveNewPost(title, body, category_id, author_id, if_display_author):
    import datetime

    new_post = db.post.insert(title = title,
                               body =body,
                               category = category,
                               post_datetime = datetime.datetime.now(),
                               author = auth_id,
                               if_display_author = if_display_author)
    db.commit()

def searchPosts(max_results, page):
    posts = db().select(db.post.ALL, limitby=((page-1) * max_results, page * max_results), orderby = "post.post_datetime DESC")
    return posts

def retrieveTagPostRel(post_list):
    post_id_list = [post.id for post in post_list]
    return db(db.post_tag_rel.post.belongs(post_id_list)).select(db.post_tag_rel.ALL, orderby = db.post_tag_rel.post|db.post_tag_rel.tag)
