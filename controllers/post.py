# -*- coding: utf-8 -*-
# try something like

# need to fix, no view, no redicr so far
def index():
    message = 'NEED TO FIX'

    return dict(message = message)

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
     return  redirect(URL('post', 'index'))
