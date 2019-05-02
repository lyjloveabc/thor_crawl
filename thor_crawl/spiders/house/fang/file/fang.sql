DROP TABLE IF EXISTS `fang_city`;
CREATE TABLE `fang_city` (
  `id`             INT(32) NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',

  `province_name`  VARCHAR(10)
  COMMENT '省份名称',
  `city_name`      VARCHAR(10)
  COMMENT '城市名称',
  `city_index_url` VARCHAR(100)
  COMMENT '城市主页地址',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '城市数据';

DROP TABLE IF EXISTS `fang_city_zone_num`;
CREATE TABLE `fang_city_zone_num` (
  `id`            INT(32) NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',

  `province_name` VARCHAR(10)
  COMMENT '省份名称',
  `city_name`     VARCHAR(10)
  COMMENT '城市名称',
  `num`           INT
  COMMENT '城市主页地址',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '城市有多少小区';

DROP TABLE IF EXISTS `fang_city_zone`;
CREATE TABLE `fang_city_zone` (
  `id`            INT(32) NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',

  `province_name` VARCHAR(10)
  COMMENT '省份名称',
  `city_name`     VARCHAR(10)
  COMMENT '城市名称',

  `first_area`    VARCHAR(10)
  COMMENT '地区名称1',
  `second_area`   VARCHAR(10)
  COMMENT '地区名称2',

  `name`          VARCHAR(50)
  COMMENT '小区名称',
  `url`           VARCHAR(100)
  COMMENT '小区主页',
  `detail_url`    VARCHAR(100)
  COMMENT '小区主页',
  `price`         VARCHAR(10)
  COMMENT '小区价格',
  `land_area`     VARCHAR(50)
  COMMENT '占地面积',
  `building_area` VARCHAR(50)
  COMMENT '建筑面积',
  `property_fee`  VARCHAR(50)
  COMMENT '物业费',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '城市有多少小区';
