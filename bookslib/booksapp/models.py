from django.db import models
from django.core import signing

# Create your models here.
# class BooksInfo(models.Model):

#     title = models.CharField(max_length=20, db_index=True)
#     author = models.CharField(max_length=10)

# class UserInfo(models.Model):

#     # 用户名
#     user_name = models.CharField('10')
#     # 用户性别
#     user_gender = models.BooleanField(default=False, )
#     born_data = models.DateField()

class LoginInfoManage(models.Manager):
    """ 登录模型管理 """
    
    def add_user(self,user_name, user_password):
        """新增用户(注册)"""
        print(user_name, user_password)
        try:
            a = LoginInfo.objects.get(user_name=user_name)
        except:
            a = LoginInfo()
            a.user_name = user_name
            a.user_password = user_password
            a.save()
            return True
        
        return False


class LoginInfo(models.Model):
    """ 登录模型 """

    # 用户名
    user_name = models.CharField(max_length=10, db_column='user', unique=True)
    # 用户密码
    user_password = models.CharField(max_length=50, db_column='password')
    # 邮箱验证
    user_vertify_code = models.IntegerField(db_column='vcode', blank=True, null=True)
    # token
    token = models.CharField(max_length=500, db_column='token',blank=True,null=True)
    # status 默认False代表未登录状态
    status = models.BooleanField(default=False)

    objects = LoginInfoManage()

    class Meta:
        db_table = 'LoginInfo'

    def __str__(self):
        return self.user_name

class AccountInfoManage(models.Manager):
    """ 账户设置模型管理 """
    def add_user(self, a_user,nickname=None,gender=None,email_num=None,address=None,phone_num=None,):
        """  传一个创设好的带user_id的用户实例(可为新创或已有)
        # 用户头像  head_image
        # 邮箱  email_num 
        # gender
        # 居住地  address
        # 手机号  phone_num
        # 昵称  nickname
        # user_id  user_id """
        try:
            if gender != a_user.gender:
                a_user.gender = gender
            if nickname != a_user.nickname:
                a_user.nickname = nickname
            if email_num!= a_user.email_num:
                a_user.email_num = email_num
            if address!= a_user.address:
                a_user.address = address
            if phone_num!= a_user.address:
                a_user.phone_num = phone_num
            a_user.save()      
        except Exception as err:
            print(err)
            return False
        else:
            return True

    def get_info(self, user_id, statusCode):
        try:
            a_user = AccountInfo.objects.get(user_id=user_id)
            user_info = {"profile":{"head_image":str(a_user.head_image),
                "email_num":  a_user.email_num ,
                "gender":a_user.gender,
                "address":a_user.address,
                "phone_num" : a_user.phone_num,
                "nickname": a_user.nickname,
                "user_id":a_user.user_id },
                "meta":{"msg":"账户信息", "status":statusCode}}
        except :
            user_info = {"profile":{},"meta":{"msg":"没有该账户","status":204}}

        return user_info

class AccountInfo(models.Model):
    """ 账户设置模型 """
    # 用户头像
    head_image = models.ImageField(width_field=None,height_field=None,upload_to='images',default='images/default.png')
    # 邮箱
    email_num = models.EmailField(null=True,blank=True, db_column='email')
    # gender False为女True为男
    gender = models.BooleanField(blank=True, null=True)
    # 居住地
    address = models.CharField(max_length=30,null=True,blank=True)
    # 手机号
    phone_num = models.CharField(max_length=11,db_column='phone',null=True,blank=True, unique=True)
    # 昵称
    nickname = models.CharField(max_length=10, unique=True,null=True,blank=True)
    # 关联账户信息
    # user = models.ForeignKey('LoginInfo',unique=True, on_delete=models.CASCADE)
    user = models.OneToOneField('LoginInfo',on_delete=models.CASCADE)

    objects = AccountInfoManage()

    class Meta:
        db_table = 'AccountInfo'

    def __str__(self):
        return self.nickname


class BooksInfoManage(models.Manager):
    """ 书籍信息管理 """

    def get_one_bookinfo(self, onebook):
        book = onebook

        try:
            image = BooksImgs.objects.get(book=book)
            image_info = {"img_name":image.image_name, "douban_url":image.douban_url}
        except:
            image_info = {"img_name":'default.png', "douban_url":'www.polimin.top/upload/media/books/default.img'}
        info ={
            "book_id" : book.id,
            "bname" : book.bname,
            "bpub_data" : str(book.bpub_data),
            "bauthor" : book.bauthor,
            "bcontent" : book.bcontent,
            "bscore" : book.bscore,
            "bnum" : book.bnum,
            "can_borrow" : book.can_borrow,
            "borrowed" : book.borrowed,
            "image_info":image_info,}
        return info

    def get_json_from_booksSet(self, books):

        try:
            binfos = {"data":[],"meta":{"msg":"书籍信息","status":200}}
            
            if books:
                for one in books:
                    binfo = self.get_one_bookinfo(one)
                    binfos["data"].append(binfo)
                return binfos
            else:
                return {"data":[],"meta":{"msg":"真的没有书了！","status":204}}

        except Exception as err:
            print(err, 'what the fuck')
            return {"data":[],"meta":{"msg":"Internal Error 500","status":500}}

    def search_by_bname(self, bname):
        print(bname)

        books = BooksInfo.objects.filter(bname__contains=bname)
        print('【by书名】',books)
        return self.get_json_from_booksSet(books)
            

    def search_by_bauthor(self, bauthor):
        books = BooksInfo.objects.filter(bauthor__contains=bauthor)
        print('【by作者】',books)
        return self.get_json_from_booksSet(books)

    def search_by_date(self, date):
        pass


    def get_all_bookinfos(self):

        books = BooksInfo.objects.all()
        return self.get_json_from_booksSet(books)

    def get_subscriber(self):
        pass

class BooksInfo(models.Model):
    """ 书籍信息 """
    # 书籍名
    bname = models.CharField(max_length=32, unique=True)
    # 书籍出版日期
    bpub_data = models.DateField(null=True)
    # 书籍作者
    bauthor = models.CharField(max_length=255, null=True)
    # 书籍基本介绍
    bcontent = models.CharField(max_length=3000, null=True,blank=True)
    # 书籍评论
    bcomment = models.CharField(max_length=500, null=True,blank=True)
    # 书籍评分 总分10
    bscore = models.FloatField(default=0,null=True, blank=True)
    # 书籍数量
    bnum = models.IntegerField(default=5)
    # 书籍可借数量
    can_borrow = models.IntegerField(default=5)
    # 书籍被借次数
    borrowed = models.IntegerField(default=0)

    objects = BooksInfoManage()

    def __str__(self):
        return self.bname


class BooksImgsManage(models.Manager):
    """ 书籍信息管理 """
    pass
class BooksImgs(models.Model):
    """ 图书图片 """
    # 图片名
    image_name = models.CharField(max_length=255, default='default.png')
    # 图片地址
    image_path = models.CharField(max_length=255, default="upload/media/books/")
    # douban_url
    douban_url = models.CharField(max_length=255, null=True, blank=True)
    # 关联图书
    book = models.OneToOneField('BooksInfo',on_delete=models.CASCADE)

    objects = BooksImgsManage()

    def __str__(self):
        return self.image_name


class BorrowInfoManage(models.Manager):
    """ 借阅信息管理 """
    def get_sub_books(self, user_id):
        try:
            a_user = BorrowInfo.objects.get(user_id=user_id)
            books = [str(i) for i in a_user.books.all()]
            info = {"data":{"user":str(user_id),"user_id":a_user.id,"books":books},"meta":{"msg":"书籍成功获取","status":200}}
        except Exception as err:
            info = {"data":err,"meta":{"msg":"书籍获取失败","status":401}}
        return info

class BorrowInfo(models.Model):
    """ 借阅信息 """
    # 信誉积分
    credit_score = models.IntegerField(default=0)
    # booker 等级 可借阅书籍数
    level = models.IntegerField(default=1)
    # 已借书籍数量
    have_borrow = models.IntegerField(default = 0)
    # 关联用户
    user = models.OneToOneField('LoginInfo',on_delete=models.CASCADE)
    # 关联借阅信息
    books = models.ManyToManyField(BooksInfo, blank=True)

    objects = BorrowInfoManage()



