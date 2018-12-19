BEGIN;

### 搜房网所有城市
DROP TABLE IF EXISTS `fang_city_area`;
CREATE TABLE `fang_city_area` (
  `id`             INT         NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`    DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`    DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `province_name`  VARCHAR(40) NULL
  COMMENT '省份名称',

  `city_name`      VARCHAR(10) NOT NULL
  COMMENT '城市名称',
  `city_index_url` VARCHAR(40) NOT NULL
  COMMENT '城市首页链接',

  `base_url`       VARCHAR(128)
  COMMENT '基础链接，后续用',

  `area_name`      VARCHAR(16) NOT NULL
  COMMENT '区域名称',
  `area_url`       VARCHAR(128)
  COMMENT '区域链接',

  `sub_name`       VARCHAR(16) NOT NULL
  COMMENT '子区域名称',
  `sub_url`        VARCHAR(128)
  COMMENT '子区域链接',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk`(`sub_url`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '搜房网所有城市';

# 搜房网-小区详情首页-原始数据
DROP TABLE IF EXISTS `fang_community`;
CREATE TABLE `fang_community` (
  `id`                  INT          NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`         DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`         DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `city_area_id`        INT          NOT NULL
  COMMENT 'fang_city_area的自增ID',
  `province_name`       VARCHAR(40)  NULL
  COMMENT '省份名称',
  `city_name`           VARCHAR(10)  NOT NULL
  COMMENT '城市名称',
  `area_name`           VARCHAR(16)  NOT NULL
  COMMENT '区域名称',
  `sub_name`            VARCHAR(16)  NOT NULL
  COMMENT '子区域名称',

  `community_index_url` VARCHAR(128) NOT NULL
  COMMENT '列表跳进来的详情主页的链接',

  `name`                VARCHAR(32)
  COMMENT '小区名称',
  `type`                VARCHAR(8)
  COMMENT '物业类别',
  `completion_time`     VARCHAR(16)
  COMMENT '建成时间',
  `price`               VARCHAR(32)
  COMMENT '小区房价',

  `address`             VARCHAR(64)
  COMMENT '小区地址',
  `building_type`       VARCHAR(64)
  COMMENT '建筑类型',
  `property_company`    VARCHAR(64)
  COMMENT '物业公司',
  `developer`           VARCHAR(64)
  COMMENT '开发商',

  `image`               VARCHAR(300)
  COMMENT '小区图片',

  `detail_url`          VARCHAR(64)
  COMMENT '小区详情链接',
  `evaluate_url`        VARCHAR(64)
  COMMENT '小区评价链接',

  PRIMARY KEY (`id`),
  UNIQUE KEY (`community_index_url`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '搜房网-小区详情首页-原始数据';

# 搜房网-小区详情首页-小区详情-原始数据
DROP TABLE IF EXISTS `fang_community_detail`;
CREATE TABLE `fang_community_detail` (
  `id`                        INT      NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `create_time`               DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `modify_time`               DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `community_id`              INT      NOT NULL
  COMMENT 'fang_community的自增ID',

  # 基本信息
  `address`                   VARCHAR(128)
  COMMENT '小区地址',
  `area`                      VARCHAR(32)
  COMMENT '所属区域',
  `postcode`                  VARCHAR(8)
  COMMENT '邮编',
  `property_description`      VARCHAR(32)
  COMMENT '产权描述',
  `property_category`         VARCHAR(8)
  COMMENT '物业类别',
  `completion_time`           VARCHAR(20)
  COMMENT '竣工时间',
  `building_type`             VARCHAR(64)
  COMMENT '建筑类别',
  `building_area`             VARCHAR(32)
  COMMENT '建筑面积',
  `floor_area`                VARCHAR(32)
  COMMENT '占地面积',
  `current_number`            VARCHAR(10)
  COMMENT '当期户数',
  `total_number`              VARCHAR(10)
  COMMENT '总户数',
  `greening_rate`             VARCHAR(10)
  COMMENT '绿化率',
  `plot_ratio`                VARCHAR(10)
  COMMENT '容积率',
  `property_fee`              VARCHAR(20)
  COMMENT '物业费',
  `property_office_telephone` VARCHAR(100)
  COMMENT '物业办公电话',
  `property_office_location`  VARCHAR(40)
  COMMENT '物业办公地点',
  `additional_information`    VARCHAR(32)
  COMMENT '附加信息',

  PRIMARY KEY (`id`),
  UNIQUE KEY (`community_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '搜房网-小区详情首页-小区详情-原始数据';

COMMIT;