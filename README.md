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
                - 商圈
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
        - 聊天
        - 留言
    - 查看房源详情
        - 附近
            - 公共设施
            - 娱乐场所
            - 通勤条件
    - 更新房源信息
    - 评价
        - 对租客
        - 对房源
            - 房主
            - 住房
    - 收藏

### 接口设计


### 数据库设计
- 用户

|属性名|类型|说明|
|--|--|--|
|uuid|varchar(50)|主键|
|tel|varchar(20)|手机|
|passwd|varchar(20)|密码|
|nickname|varchar(20)|昵称|
|email|varchar(20)|邮箱|
|identify_code|varchar(20)|身份证|
|type|varchar(20)|租户/房东|
|icon||头像url连接|

- 房屋信息

|属性名|类型|说明|
|--|--|--|
|uuid|..|..|
|user_id|||
|location|||
|city|||
|house_type|||
|rent_amount|||
|latitude|||
|longtitude|||
|size|||
|is_co_rent|||
|detail|||
|rank|||
|name|||

- 订单信息

||||
|--|--|--|
|uuid|||
|user_id||||
|room_id||||
|create_time||||
|rent_time|||

- 留言

||||
|--|--|--|
|uuid|||
|room_id|||
|user_id|||
|content|||
|post_time|||

- 聊天

||||
|--|--|--|
|uuid|||
|user_id|||
|room_id|||
|content|||
|post_time|||

- 评价

||||
|--|--|--|
|uuid|||
|user_id|||
|user_id|||
|content|||
|create_time|||

- 图

||||
|--|--|--|
|uuid|||
|url|||