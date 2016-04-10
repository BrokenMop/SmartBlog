# -*- coding: utf-8 -*-
# try something like

# need to fix, no view, no redicr so far
def index():
    max_results = 10
    page = 1
    posts = db().select(db.post.ALL, limitby=((page-1) * max_results, page * max_results), orderby = "post.post_datetime DESC")

    # response variables:
    # posts label_posted_by  label_tags label_read_more label_comments

    return dict(posts = posts,
                label_posted_by = T('Posted by'),
                label_tags = T('Tags'),
                label_read_more = T('Read more'),
                label_comments = T('Comments')
                )

#@auth.requires(lambda: auth.has_membership(ADMIN_GROUP) or auth.has_membership(AUTUOR_GROUP))
def new():
    categories = getAllCategoriesWithCount()
    return dict(categories = categories)

# unauth user proof
#@auth.requires(lambda: auth.has_membership(ADMIN_GROUP) or auth.has_membership(AUTUOR_GROUP))
def save():
     category = request.vars['post-category']
     title = request.vars['post-title']
     if_display_author = request.vars['if-display-author']

     import datetime
     import HTMLParser
     post_body =  HTMLParser.HTMLParser().unescape(unicode(request.vars['post-body'],"utf-8"))
     new_post = db.post.insert(title = title,
                               body =post_body,
                               category = category,
                               post_datetime = datetime.datetime.now(),
                               author = auth.user,
                               if_display_author = if_display_author)
     db.commit()
     return  redirect(URL('post', vars={'pid':new_post.id}))
