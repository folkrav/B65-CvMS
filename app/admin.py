from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from .models import User, ArticleStatus, ArticleCategory, PrivilegeGroup
from flask_login import current_user
from decorators import privileges_required

class UserView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

    def is_accessible(self):
        return current_user.is_administrator()

class ArticleView(UserView):
    column_list = ('id', 'category', 'status', 'title', 'summary', 'body', 'image_path', 'link_url', 'timestamp')
