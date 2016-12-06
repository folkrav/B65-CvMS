from flask_admin.contrib.sqla import ModelView
from .models import User, ArticleStatus, ArticleCategory

class UserView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False

class ArticleView(ModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'category', 'status', 'title', 'summary', 'body', 'image_path', 'link_url', 'timestamp')
