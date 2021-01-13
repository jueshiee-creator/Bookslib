from django.contrib import admin
from booksapp.models import LoginInfo,AccountInfo,BooksInfo,BooksImgs ,BorrowInfo

# Register your models here.
class LoginInfoAdmin(admin.ModelAdmin):
    """ 用户登录后台管理 """

    list_display = ['id', 'user_name', 'user_password', 'token']

class AccountInfoAdmin(admin.ModelAdmin):
    """ 账户信息后台管理 """

    list_display = ['id','head_image','email_num','gender','address','phone_num','nickname','user_id']

class BooksInfoAdmin(admin.ModelAdmin):
    """ 书籍信息后台管理 """

    list_display = ['bname','bpub_data','bauthor','bscore','borrowed']

class BorrowInfoAdmin(admin.ModelAdmin):
    """ 借阅信息后台管理 """

    list_display = ['user_id','credit_score','level','have_borrow'] 

class BooksImgsAdmin(admin.ModelAdmin):
    """  图书图片信息后台管理 """

    list_display = ['image_name','image_path']


# 在后台注册信息
admin.site.register(LoginInfo, LoginInfoAdmin)
admin.site.register(AccountInfo, AccountInfoAdmin)
admin.site.register(BooksInfo, BooksInfoAdmin)
admin.site.register(BorrowInfo, BorrowInfoAdmin)
admin.site.register(BooksImgs, BooksImgsAdmin)
