from booksapp import views
# from booksapp.views import BookInfoAPI
from django.urls import path, re_path

urlpatterns = [
    re_path(r'^$',views.get_all_books, name='all_books'),
    re_path(r'^login$', views.login),  # 登录
    re_path(r'^login/alter$', views.password_alter),  # 修改密码
    re_path(r'^register$', views.register, name='register'),  # 注册
    re_path(r'^logout$', views.logout, name='logout'),  # 登出
    re_path(r'^login/status$', views.login_status, name='status'),  # 登录状态

    re_path(r'^avatar/upload$', views.upload_image, name='upload'),  # 上传头像
    re_path(r"^upload/media/(images|books)/(.*)$", views.get_img, name=  "images"),  # 获取照片
    re_path(r'^account$',views.account,name='account'),  # 账户信息获取
    re_path(r'^account/alter$',views.save_account,name='account_alter'),  # 更改账户信息

    re_path(r'^bookname/(.*)$', views.get_id_by_name,name='book_id'),  # 通过书名得到书的id 自己用
    re_path(r'^borrow/books$', views.get_sub_books,name='bookinfo_by_id'),  # 通过书名得到书的id
    re_path(r'^all/books/infos$',views.get_all_books, name='all_books'),  # 所有书籍信息
    re_path(r'^book/search$',views.search_book, name='one_book_search'),  # 搜索书籍信息
    

]