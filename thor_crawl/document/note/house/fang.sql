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