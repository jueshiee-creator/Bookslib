import json, time
import hashlib
from django.shortcuts import render, HttpResponse
# from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import signing

from booksapp.models import LoginInfo,AccountInfo,BooksInfo,BorrowInfo
# Create your views here.

HEADER={
    'type':'JWT',
    'alg':'HS256'
}

def Encrypt(value):
    data=signing.dumps(value)
    data=signing.b64_encode(data.encode()).decode()
    return data
 
def Decrypt(value):
    data=signing.b64_decode(value.encode()).decode()
    data=signing.loads(data)
    return data
 
def Token(headers,payloads):
    header=Encrypt(headers)
    payload=Encrypt(payloads)
    md5=hashlib.md5()
    md5.update(("%s.%s"%(header,payload)).encode())
    signature=md5.hexdigest()
    token="%s.%s.%s"%(header,payload,signature)
    return token

def hash_decrypt(str):
    m = hashlib.md5()
    b = str.encode(encoding='utf-8')
    m.update(b)
    str_md5 = m.hexdigest()
    return str_md5

def csrf_setting(response):
    response["Access-Control-Allow-Origin"] = "http://localhost:8080" 
    # response["Access-Control-Allow-Origin"] = "null"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS" 
    response["Access-Control-Max-Age"] = "3600" 
    response["Access-Control-Allow-Headers"] = "*" 
    response["Access-Control-Allow-Credentials"]="True"
    return response

def get_post_data(request):
    """ 获取get,post数据 """
    if request.method == 'GET':
        data = request.GET
    if request.method == 'POST':
        try:
            data = request.body.decode('utf8')
            data = json.loads(data)
        except:
            data = request.POST
    return data

# @ensure_csrf_cookie
def login(request):
    """ 登录 """

    def verify(user, password):
        try:
            u = LoginInfo.objects.get(user_name=user)
        except:
            return False
        else:
            # print(type(password), password)
            u_password = u.user_password
            password = hash_decrypt(password)

        return str(u_password) == str(password)

    # print(request)

    from_data = get_post_data(request)

    print(from_data) 
    
    user = str(from_data.get('user'))
    password = str(from_data.get('password'))

    if verify(user, password):
        
        a_user = LoginInfo.objects.get(user_name=user)
        id,status = a_user.id, True

        code, msg = 201, '登录成功'
        headers = HEADER
        payloads={'iss': user, 'iat':time.time()}
        token=Token(headers,payloads)

        a_user.token = token
        a_user.status = True
        a_user.save()

        print('token-long:',len(token))

    else:
        id, status = '', False
        code,msg,token = 302, '用户名或密码错误，登录失败', ''

    users = {
        'data':{'id':id,'username':user,'token':token,"status":status
        },
        'meta':{'msg':msg,'status': code,
        }   
    }
    j = json.dumps(users)

    response = HttpResponse(j, content_type='application/json')
    response = csrf_setting(response)
    response.set_cookie('ctoken',value =token,max_age = 3600,expires = None,domain=None,path ='/',secure=False,httponly = False,samesite = None)

    return response

def login_status(request):
    """ 返回登录信息 id，status"""
    from_data = get_post_data(request)

    print(from_data)
    user = from_data.get('user')
    try:
        a_user = LoginInfo.objects.get(user_name=user)
        id_ = a_user.id
        user_status = a_user.status
        user_info = {'data':{'id':id_,'user':user,'status':user_status},
        'meta':{'msg':'信息获取成功','status': 200,}  }
    except:
        user_info = {'data':{},'meta':{'msg':'没有该用户信息','status':204}}

    user_info = json.dumps(user_info)

    response = HttpResponse(user_info, content_type='application/json')
    return response

def register(request):
    """ 注册 """
    from_data = get_post_data(request)

    print(request)
    print(from_data)
    user = str(from_data.get('user'))
    password = str(from_data.get('password'))

    print(user, password)

    password = hash_decrypt(password)
    ver = LoginInfo.objects.add_user(user, password)
    if ver:
        id = LoginInfo.objects.get(user_name=user).id
        code, msg = 201, '注册成功'
    else:
        id = ''
        code,msg = 302, '用户名已被占用，注册失败'

    users = {
        'data':{'id':id,'username':user,"status":False
        },
        'meta':{'msg':msg,'status': code,
        }     
    }
    j = json.dumps(users)
    
    return HttpResponse(j, content_type='application/json')

def logout(request):
    """ release login status """
    from_data = get_post_data(request)

    user_name = from_data.get('user', None)
    headers = HEADER
    payloads={'iss': user_name, 'iat':time.time()}
    token=Token(headers,payloads)

    a_user = LoginInfo.objects.get(user_name=user_name)
    id = a_user.id
    a_user.token = token
    a_user.status = False
    a_user.save()

    users = {
        'data':{'id':id,'username':user_name,"status":False
        },
        'meta':{'msg':'成功登出','status': 200,
        }     
    }
    j = json.dumps(users)

    response = HttpResponse(j, content_type='application/json')
    response.delete_cookie("ctoken")
    # response = csrf_setting(response)
    return response

def password_alter(request):
    """ 用户密码修改 """
    data = get_post_data(request)

    user = data.get('user')

    pre_password = hash_decrypt(data.get('pre_password'))
    new_password = hash_decrypt(data.get('new_password')) 

    try:
        a_user = LoginInfo.objects.get(user_name=user)
        d_password = a_user.user_password

        if str(d_password) == str(pre_password):
            a_user.user_password = new_password
            id_ = a_user.id
            status = a_user.status
            a_user.save()
            user_info = {
                'data':{'id':id_,'username':user,"status":status
                },
                'meta':{'msg':"修改密码成功",'status': 200,
                }   
            }
        else:
            return HttpResponse('密码输入错误')
    except:
        user_info = {"msg":"Internal Error","status":500}
    j = json.dumps(user_info)

    return HttpResponse(j, content_type='application/json')

def upload_image(request):
    """ 上传头像 """
    # if request.method == 'GET':
    #     data = request.GET
    # if request.method == 'POST':
    #     data = request.POST
    try:
        image = request.FILES["file"]
        print(image)
    except:
        return HttpResponse('301')
    try:
        token = request.COOKIES["ctoken"]
    except:
        return HttpResponse('Have No Account 400')
    # print(request.COOKIES["ctoken"])
    try:
        a_user = LoginInfo.objects.get(token=token)
        user_id = a_user.id
    except:
        return HttpResponse(400)

    try:
        ac_user = AccountInfo.objects.get(user_id=user_id)
    except:
        ac_user = AccountInfo()
        ac_user.user_id = user_id
    
    ac_user.head_image = image
    ac_user.save()

    res_data = {"meta":{"msg":"添加或更改成功","status":201}}
    res_data = json.dumps(res_data)

    response = HttpResponse(res_data)
    response = csrf_setting(response)
    return response

def get_img(request, imgpath,img):
    """ img """
    with open('upload/media/{}/{}'.format(imgpath,img), 'rb') as f:
        image = f.read()
    return HttpResponse(image, content_type="image/png") 

##########################################################################################
####################################账户设置##############################################
def save_account(request):
    """ 保存账户设置 """
    data = get_post_data(request)

    cookies = request.COOKIES
    print(cookies)

    try:
        token = cookies['ctoken']
        user_id = LoginInfo.objects.get(token=token).id
    except:
        return HttpResponse('Not to login or Cookies over time')

    try:
        a_user = AccountInfo.objects.get(user_id = user_id)
        statusCode = 200
    except:
        a_user = AccountInfo()
        a_user.user_id = user_id
        statusCode = 201
    
    xlist = ["email_num","gender","address","phone_num","nickname"]
    profile = {}
    for i in xlist:
        profile[i] = data.get(i)

    Bool = AccountInfo.objects.add_user(a_user,**profile)

    if Bool:
        user_info = AccountInfo.objects.get_info(user_id,statusCode)
    else:
        user_info = {"data":{},"meta":{"msg":"添加或更改失败","status":301}}
    user_info = json.dumps(user_info)

    return HttpResponse(user_info, content_type='application/json')


def account(request):
    """ 获取账户信息 """
    # get_post_data()

    cookies = request.COOKIES
    try:
        token = cookies['ctoken']
        print(token)
        user_id = LoginInfo.objects.get(token=token)
    except:
        return HttpResponse('Not to login or Cookies over time')

    statusCode = 200
    user_info = AccountInfo.objects.get_info(user_id,statusCode)

    user_info = json.dumps(user_info)

    return HttpResponse(user_info, content_type='application/json')


def get_id_by_name(request,bookname):
    """ get book id by bookname """
    book = BooksInfo.objects.get(bname=bookname)
    book_id = book.id
    return HttpResponse(book_id)


def get_all_books(request):
    """ 获取全部书籍信息 """
    infos = BooksInfo.objects.get_all_bookinfos()
    infos = json.dumps(infos)
    return HttpResponse(infos, content_type='application/json')
    

def search_book(request):
    """ 搜索书籍 """
    # from collections import ChainMap
    data = get_post_data(request)
    q = data.get('search_text')

    book_name = BooksInfo.objects.search_by_bname(q)
    book_author= BooksInfo.objects.search_by_bauthor(q)

    # print(book_name)
    # print(book_author)
    infos = dict()
    if book_name["data"]:
        infos.update(book_name)
    
    if book_author["data"]:
        infos.update(book_author)

    if not infos:
        return HttpResponse('Have No Books')
    else:
        
        infos = json.dumps(infos)
        return HttpResponse(infos, content_type='application/json')



def get_sub_books(request):
    """ 获取用户订阅的书籍 """
    # data = get_post_data(request)

    cookies = request.COOKIES
    try:
        token = cookies['ctoken']
        user_id = LoginInfo.objects.get(token=token)
    except:
        return HttpResponse('Not to login or Cookies over time')

    books = BorrowInfo.objects.get_sub_books(user_id)
    print(books)

    books = json.dumps(books)
    response = HttpResponse(books, content_type='application/json')
    return response