### 安居客所有城市
DROP TABLE IF EXISTS `ajk_city`;
CREATE TABLE `ajk_city` (
  `id`          INT         NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time` DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time` DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `name`        VARCHAR(16) NOT NULL
  COMMENT '城市名称',
  `url`         VARCHAR(32) NOT NULL
  COMMENT '城市名称',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客所有城市';

### 安居客城市的新房、二手房首页地址，即新房、二手房的入口
DROP TABLE IF EXISTS `ajk_city_inlet`;
CREATE TABLE `ajk_city_inlet` (
  `id`          INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time` DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time` DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `city_id`     INT          NOT NULL
  COMMENT '城市ID',
  `city_name`   VARCHAR(16)  NOT NULL
  COMMENT '城市名称',
  `type`        VARCHAR(8)   NOT NULL
  COMMENT '所属类型，枚举：NEW、SECOND',
  `url`         VARCHAR(128) NOT NULL
  COMMENT '链接地址',
  `total`       SMALLINT     NULL
  COMMENT '楼盘总数',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客城市的新房、二手房首页地址，即新房、二手房的入口';

### 安居客城市的新房、二手房的所有区域
DROP TABLE IF EXISTS `ajk_city_area`;
CREATE TABLE `ajk_city_area` (
  `id`              INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`     DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`     DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `city_inlet_id`   INT          NOT NULL
  COMMENT '入口ID',
  `city_inlet_type` VARCHAR(8)   NOT NULL
  COMMENT '所属类型，枚举：NEW、SECOND',
  `city_name`       VARCHAR(16)  NOT NULL
  COMMENT '城市名称',
  `area_name`       VARCHAR(16)  NOT NULL
  COMMENT '区域名称',
  `area_url`        VARCHAR(128) NOT NULL
  COMMENT '区域名称',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客城市的新房、二手房的所有区域';

### 安居客二手房小区
DROP TABLE IF EXISTS `ajk_second_community`;
CREATE TABLE `ajk_second_community` (
  `id`             INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`    DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`    DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `city_area_id`   INT          NOT NULL
  COMMENT '城市区域ID',
  `city_name`      VARCHAR(16)  NOT NULL
  COMMENT '城市名称',
  `area_name`      VARCHAR(16)  NOT NULL
  COMMENT '区域名称',
  `community_name` VARCHAR(32)  NOT NULL
  COMMENT '小区名称',
  `url`            VARCHAR(128) NOT NULL
  COMMENT '详情地址',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客二手房小区';