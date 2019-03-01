## 产品原型
### 功能需求
- 功能
    - 登录 
    - 注册 
    - 找回密码 
    - 信息修改 
    - 发布房源 
    - 搜索 
    - 筛选
        - 根据条件
            - 地理位置
                - 城市
                - 小区
            - 户型
            - 价格
            - 楼层
            - 是否合租
    - 租赁 
        - 订单      
        - 支付
            - 押金
            - 房费
        - 合同
            - 一式三份
    - 退租 
    - 交流 
        - 留言 
    - 查看房源详情
        - 附近
            - 公共设施
            - 娱乐场所
            - 通勤条件
    - 更新房源信息
    - 评价 -
        - 对租客
        - 对房源
            - 房主
            - 住房
    - 收藏

### 接口设计
- 房屋
    - 根据筛选条件查询房屋(list)
        - 返回
            - 房屋id
            - 城市
            - 区
            - 地点（小区/location）
            - 价格
            - 名称
    - 根据房屋id查询房屋
        - 返回
            - 房屋所有信息
            - 房东信息
            - 评价
            - 房屋图片
    - CUD
- 用户
    - 创建
    - 更新
    - 查找
    - 删除
- 订单
    - CURD
- 留言
    - CURD
- 评价
    - CURD

### 数据库设计
- 用户

|属性名|类型|说明|
|--|--|--|
|uuid|varchar(50)|主键|
|tel|varchar(20)|手机|
|passwd|varchar(20)|密码|
|nickname|varchar(20)|昵称|
|email|varchar(50)|邮箱|
|identify_code|varchar(20)|身份证|
|type|varchar(20)|租户/房东|
|icon|varchar(255)|头像url连接|

- 房屋信息

|属性名|类型|说明|
|--|--|--|
|uuid|varchar(50)|房屋id|
|user_id|varchar(50)|房东id|
|location|varchar(20)|房屋地址|
|city|varchar(20)|房屋城市|
|district|varchar(20)|所在区|
|house_type|varchar(20)|房屋类型|
|rent_amount|int|租金价格|
|latitude|varchar(20)|纬度|
|longtitude|varchar(20)|经度|
|size|varchar(20)|房屋大小|
|is_co_rent|varchar(20)|是否合租|
|detail|varchar(255)|房屋细节|
|rank|varchar(20)|房屋排名|
|name|varchar(20)|房屋名称|
|state|varchar(20)|房屋状态(是否被租)|  
|floor|int|楼层|

- 订单信息

||||
|--|--|--|
|uuid|varchar(50)|订单id|
|user_id|varchar(50)|租客id|
|room_id|varchar(50)|房间id|
|create_time|date|订单创建时间|
|rent_time|varchar(20)|租赁时长|  
|is_over|int|订单状态|(0, 'wait for pay'),(1, 'wait for comment'),(2, 'complete')  
|status|int|1上架0下架|  


- 留言

||||
|--|--|--|
|uuid|varchar(50)|主键|
|room_id|varchar(50)|房间id|
|user_id|varchar(50)|用户id|
|content|varchar(1024)|留言内容|
|post_time|date|留言时间|

- 聊天

||||
|--|--|--|
|uuid|varchar(50)|主键|
|renter_id|varchar(50)|租客id|
|rentee_id|varchar(50)|房东id|
|content|varchar(1024)|聊天内容|
|post_time|date|发送时间|

- 评价

||||
|--|--|--|
|uuid|varchar(50)|主键|
|renter_id|varchar(50)|租客id|
|rentee_id|varchar(50)|房东id|
|content|varchar(1024)|评论内容|
|create_time|date|评论时间|

- 房屋图片

||||
|--|--|--|
|uuid|varchar(50)|主键|
|room_id|varchar(50)|房屋主键|
|url|varchar(255)|图片url|