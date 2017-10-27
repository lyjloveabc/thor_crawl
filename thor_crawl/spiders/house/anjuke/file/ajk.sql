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

  `name`        VARCHAR(16)  NOT NULL
  COMMENT '城市名称',
  `type`        VARCHAR(8)   NOT NULL
  COMMENT '区域所属类型，枚举：NEW、SECOND',
  `url`         VARCHAR(128) NOT NULL
  COMMENT '链接地址',
  `total`       SMALLINT     NOT NULL DEFAULT NULL
  COMMENT '楼盘总数',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客城市的新房、二手房首页地址，即新房、二手房的入口';

### 安居客城市的新房、二手房的所有区域
DROP TABLE IF EXISTS `ajk_city_area`;
CREATE TABLE `ajk_city_area` (
  `id`            INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`   DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`   DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `city_name`     VARCHAR(16)  NOT NULL
  COMMENT '城市名称',
  `city_url_type` VARCHAR(8)   NOT NULL
  COMMENT '城市链接所属类型，枚举：NEW、SECOND',
  `area_name`     VARCHAR(16)  NOT NULL
  COMMENT '区域名称',
  `area_url`      VARCHAR(128) NOT NULL
  COMMENT '区域名称',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客城市的新房、二手房的所有区域';