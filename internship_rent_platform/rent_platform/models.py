from django.db import models


# Create your models here.

class User(models.Model):
    '''
    `uuid` varchar(50) not null,
    `tel` varchar(20) not null,
    `passwd` varchar(20) not null,
    `nickname` varchar(20),
    `email` varchar(50),
    `identify_code` varchar(20),
    `utype` varchar(20),
    `icon` varchar(255),
    primary key (`uuid`) using btree
    '''
    tel = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    identify_code = models.CharField(max_length=20, null=True)
    utype = models.CharField(max_length=20, null=True)
    icon = models.CharField(max_length=255, null=True)


class Room(models.Model):
    '''
    `uuid` varchar(50) not null,
    `user_id` varchar(50) not null,
    `location` varchar(20),
    `city` varchar(20),
    `district` varchar(20),
    `rent_amount` varchar(20),
    `latitude` varchar(20),
    `longtitude` varchar(20),
    `size` varchar(20),
    `is_co_rent` varchar(20),
    `detail` varchar(255),
    `rank` varchar(20),
    `name` varchar(20),
    `state` varchar(20),
    primary key (`uuid`) using btree
    '''
    user_id = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    district = models.CharField(max_length=20)
    rent_amount = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    longtitude = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    is_co_rent = models.CharField(max_length=20)
    detail = models.CharField(max_length=255)
    rank = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    state = models.CharField(max_length=20)


class Order(models.Model):
    '''
     `uuid` varchar(50) not null,
    `user_id` varchar(50) not null,
    `room_id` varchar(50) not null,
    `create_time` date,
    `rent_time` varchar(20),
    primary key (`uuid`) using btree
    '''
    user_id = models.CharField(max_length=50, null=False)
    room_id = models.CharField(max_length=50, null=False)
    create_time = models.DateField()
    rent_time = models.CharField(max_length=20)


class Message(models.Model):
    '''
    `uuid` varchar(50) not null,
    `user_id` varchar(50) not null,
    `room_id` varchar(50) not null,
    `content` varchar(1024),
    `post_time` date,
    primary key (`uuid`) using btree
    '''
    user_id = models.CharField(max_length=50, null=False)
    room_id = models.CharField(max_length=50, null=False)
    content = models.CharField(max_length=1024)
    post_time = models.DateField()


class Chat(models.Model):
    '''
    `uuid` varchar(50) not null,
    `renter_id` varchar(50) not null,
    `rentee_id` varchar(50) not null,
    `content` varchar(1024),
    `post_time` date,
    primary key (`uuid`) using btree
    '''
    renter_id = models.CharField(max_length=50, null=False)
    rentee_id = models.CharField(max_length=50, null=False)
    content = models.CharField(max_length=1024)
    post_time = models.DateField()


class Comment(models.Model):
    '''
    `uuid` varchar(50) not null,
    `renter_id` varchar(50) not null,
    `rentee_id` varchar(50) not null,
    `content` varchar(1024),
    `create_time` date,
    primary key (`uuid`) using btree
    '''
    renter_id = models.CharField(max_length=50, null=False)
    rentee_id = models.CharField(max_length=50, null=False)
    content = models.CharField(max_length=1024)
    create_time = models.DateField()


class Img(models.Model):
    '''
     `uuid` varchar(50) not null,
    `room_id` varchar(50) not null,
    `url` varchar(255),
    primary key (`uuid`) using btree
    '''
    room_id = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
