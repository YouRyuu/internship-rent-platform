SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `user`;
create table `user`(
    `uuid` varchar(50) not null,
    `tel` varchar(20) not null,
    `passwd` varchar(20) not null,
    `nickname` varchar(20),
    `email` varchar(50),
    `identify_code` varchar(20),
    `type` varchar(20),
    `icon` varchar(255),
    primary key (`uuid`) using btree
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

drop table if EXISTS `room`;
create table `room`(
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

drop table if  EXISTS `order`;
create table `order`(
    `uuid` varchar(50) not null,
    `user_id` varchar(50) not null,
    `room_id` varchar(50) not null,
    `create_time` date,
    `rent_time` varchar(20),
    primary key (`uuid`) using btree
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

drop table if EXISTS `message`;
create table `message`(
    `uuid` varchar(50) not null,
    `user_id` varchar(50) not null,
    `room_id` varchar(50) not null,
    `content` varchar(1024),
    `post_time` date,
    primary key (`uuid`) using btree
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

drop table if EXISTS `chat`;
create table `chat`(
    `uuid` varchar(50) not null,
    `renter_id` varchar(50) not null,
    `rentee_id` varchar(50) not null,
    `content` varchar(1024),
    `post_time` date,
    primary key (`uuid`) using btree
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

drop table if EXISTS `comment`;
create table `comment`(
    `uuid` varchar(50) not null,
    `renter_id` varchar(50) not null,
    `rentee_id` varchar(50) not null,
    `content` varchar(1024),
    `create_time` date,
    primary key (`uuid`) using btree
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

drop table if EXISTS `img`;
create table `img`(
    `uuid` varchar(50) not null,
    `room_id` varchar(50) not null,
    `url` varchar(255),
    primary key (`uuid`) using btree
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;