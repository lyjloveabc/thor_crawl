### 安居节课房源数据
DROP TABLE IF EXISTS `ajk_hz_area`;
CREATE TABLE `ajk_hz_area` (
  `id`          INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time` DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time` DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `base_url`    VARCHAR(128) NOT NULL DEFAULT ''
  COMMENT 'url代码',
  `name`        VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT 'url代码',


  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客杭州，所有的地区';

DROP TABLE IF EXISTS `ajk_hz_community`;
CREATE TABLE `ajk_hz_community` (
  `id`                  INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`         DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`         DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `hz_area_id`          INT          NOT NULL
  COMMENT '地区ID',
  `hz_area_name`        VARCHAR(16)
  COMMENT '地区名称',
  `url`                 VARCHAR(128) NOT NULL DEFAULT ''
  COMMENT 'url',
  `name`                VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '小区名称',
  `community_address`   VARCHAR(64)
  COMMENT '地区地址',
  `village_house_price` VARCHAR(32)
  COMMENT '小区房价',
  `date`                VARCHAR(32)
  COMMENT '竣工时间',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客杭州，小区';

DROP TABLE IF EXISTS `ajk_hz_community_detail`;
CREATE TABLE `ajk_hz_community_detail` (
  `id`                  INT      NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`         DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`         DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `hz_area_id`          INT      NOT NULL
  COMMENT '地区ID',
  `hz_area_name`        VARCHAR(16)
  COMMENT '地区名称',
  `community_name`      VARCHAR(32)
  COMMENT '小区名称',
  `community_address`   VARCHAR(64)
  COMMENT '小区地址',

  `property_type`       VARCHAR(64)
  COMMENT '物业类型',
  `property_fee`        VARCHAR(64)
  COMMENT '物业费',
  `total_area`          VARCHAR(64)
  COMMENT '总建面积',
  `total_house`         VARCHAR(64)
  COMMENT '总户数',
  `build_year`          VARCHAR(64)
  COMMENT '建造年代',
  `parking`             VARCHAR(64)
  COMMENT '停车位数量',
  `plot_ratio`          VARCHAR(64)
  COMMENT '容积率',
  `developer`           VARCHAR(64)
  COMMENT '开发商',
  `property_company`    VARCHAR(64)
  COMMENT '物业公司',

  `second-hand_count`   VARCHAR(32)
  COMMENT '二手房源数',
  `rent_count`          VARCHAR(32)
  COMMENT '租房源数',
  `village_house_price` VARCHAR(32)
  COMMENT '小区房价',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk`(`hz_area_id`, `community_name`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '安居客杭州，小区的详情';


SELECT
  ifnull(hz_area_name, '')        AS '地区',
  ifnull(name, '')                AS '小区名称',
  ifnull(community_address, '')   AS '小区地址',
  ifnull(village_house_price, '') AS '小区房价',
  ifnull(date, '')                AS '竣工时间'

FROM ajk_hz_community
ORDER BY hz_area_id;

SELECT
  ifnull(hz_area_name, '')        AS '地区',
  ifnull(community_name, '')      AS '小区名称',
  ifnull(community_address, '')   AS '小区地址',
  ifnull(village_house_price, '') AS '小区房价',
  ifnull(property_type, '')       AS '物业类型',
  ifnull(property_fee, '')        AS '物业费',
  ifnull(total_area, '')          AS '总建面积',
  ifnull(total_house, '')         AS '总户数',
  ifnull(build_year, '')          AS '建造年代',
  ifnull(parking, '')             AS '停车位数量',
  ifnull(plot_ratio, '')          AS '容积率',
  ifnull(developer, '')           AS '开发商',
  ifnull(property_company, '')    AS '物业公司'

FROM ajk_hz_community_detail
ORDER BY hz_area_id;