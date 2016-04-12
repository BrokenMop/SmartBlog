# -*- coding: utf-8 -*-
# try something like

# need to fix, no view, no redicr so far
def index():
    message = 'NEED TO FIX'

    return dict(message = message)

#@auth.requires(lambda: auth.has_membership(ADMIN_GROUP) or auth.has_membership(AUTUOR_GROUP))
def new():
    categories = getAllPostCategoriesWithCount()
    return dict(categories = categories)

# unauth user proof
#@auth.requires(lambda: auth.has_membership(ADMIN_GROUP) or auth.has_membership(AUTUOR_GROUP))
def save():
    category_id = request.vars['post-category']
    title = request.vars['post-title']
    if_display_author = request.vars['if-display-author']

    import HTMLParser
    body =  HTMLParser.HTMLParser().unescape(unicode(request.vars['post-body'],"utf-8"))

    saveNewPost(title, body, category_id, auth.user, if_display_author)
    return  redirect(URL('default', 'index'))
