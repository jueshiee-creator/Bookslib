# bookslib

### Login(登录)

> 说明：登录接口
>
> ##### 请求地址：'/login'
>
> **调用例子**：`/login?user=234&password=345`
>
> code为201表示登录成功，302表示登录失败

### Register（注册）

> 说明：注册接口
>
> ##### 请求地址：'/register'
>
> **调用例子**：`/register?user=234&password=345`
>
> code为201表示注册成功，302表示注册用户名已存在

### [退出登录](https://binaryify.github.io/NeteaseCloudMusicApi/#/?id=退出登录)

> 说明 : 调用此接口 , 可退出登录
>
> **调用例子 :** `/logout`

### 登录状态信息

> 说明 : 获取登录信息
>
> **调用例子 :**`/login/status?user=123`

### 用户头像上传

> 说明 : 用户信息头像上传  GET/POST
>
> **调用例子 :**`/avatar/upload`

### 书籍/头像   图片获取

> 说明 : 获取图片 GET/POST
>
> **调用例子 :**`/upload/media/(images|books)/图片名`

### 用户信息获取

> 说明：账户信息接口
>
> ##### 请求地址：'/account'
>
> **调用例子:** `/account`
>
> ```python
>cookie带有token信息确认身份
> ```
> 

### 用户信息管理

> 说明：账户信息更改接口(也可用为初始设置)
>
> **请求方式：** GET/POST
>
> ##### 请求地址：'/account/alter'
>
> **调用例子:** `/account/alter?nickname='jue'&gender=0`
>
> ```python
> 参数（5）：
> # 邮箱 email_num
> # gender=""  False为女  （必填）
> #居住地 address
> # 手机号 phone_num
> # 昵称 nickname  （必填）
> 
>  user_id user_id   （cookie加持token确认身份信息）
> ```
>

### 书籍信息管理

> 说明：获取书籍  
>
> **请求方式：** GET/POST
>
> ##### **请求地址:** 	
>
> - 全部书籍：`all/books/infos`
> - 搜索书籍：例子：`/book/search?search_text=人生海海`
>
> ```python
> 返回json数据
> {
>     "data":[书籍信息],
>     "mate":{}
> }
> ```
>