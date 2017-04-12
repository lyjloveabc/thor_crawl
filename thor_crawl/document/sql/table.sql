### 陆金所所有基金
DROP TABLE IF EXISTS `lu_fund`;
CREATE TABLE `lu_fund` (
  `id`                          INT(32)      NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`                  DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`                  DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `code`                        VARCHAR(128) NOT NULL DEFAULT '0'
  COMMENT '基金代码',
  `simple_name`                 VARCHAR(128)
  COMMENT '基金简称',
  `latest_net_value`            VARCHAR(32)
  COMMENT '最新净值',
  `latest_net_value_date`       VARCHAR(32)
  COMMENT '最新净值',
  `day_of_growth`               VARCHAR(32)
  COMMENT '日增长率',
  `nearly_a_month`              VARCHAR(32)
  COMMENT '近一个月',
  `nearly_three_months`         VARCHAR(32)
  COMMENT '近三个月',
  `almost_a_year`               VARCHAR(32)
  COMMENT '近一年',
  `since_this_year`             VARCHAR(32)
  COMMENT '今年以来',
  `since_set_up`                VARCHAR(32)
  COMMENT '成立以来',
  `investment_amount_threshold` VARCHAR(32)
  COMMENT '起投金额（元）',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '权限表 lu_fund';

### 中国轴承产业服务平台 商品类目表
DROP TABLE IF EXISTS `bearing_zc_goods_category`;
CREATE TABLE `bearing_zc_goods_category` (
  `id`         INT(32)  NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `name`       VARCHAR(32)
  COMMENT '商品类目名称',
  `url`        VARCHAR(256)
  COMMENT '商品类目所含商品的URL',
  `status`     CHAR(1)  NOT NULL DEFAULT '0'
  COMMENT '状态',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '中国轴承产业服务平台 商品类目表';

### 中国轴承产业服务平台 商品表
DROP TABLE IF EXISTS `bearing_zc_goods`;
CREATE TABLE `bearing_zc_goods` (
  `id`                     INT(32)  NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`             DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`             DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `name`                   VARCHAR(64)
  COMMENT '商品名称',
  `category_id`            INT(32)
  COMMENT 'category_id',
  `category_name`          VARCHAR(32)
  COMMENT '商品类目名称',
  `model`                  VARCHAR(64)
  COMMENT '商品型号',
  `detail_url`             VARCHAR(128)
  COMMENT '商品详情的URL',

  `images`                 VARCHAR(256)      DEFAULT ''
  COMMENT '商品图片',
  `minimum_order_quantity` VARCHAR(32)       DEFAULT ''
  COMMENT '起订数量：1（套）',
  `warranty_time`          VARCHAR(32)       DEFAULT ''
  COMMENT '质保时间：正品',
  `brand`                  VARCHAR(32)       DEFAULT ''
  COMMENT '品牌：SKF',
  `price`                  VARCHAR(32)       DEFAULT ''
  COMMENT '价格：1.00（元）',
  `volume`                 VARCHAR(32)       DEFAULT ''
  COMMENT '成交量：0（套）',
  `release_time`           VARCHAR(32)       DEFAULT ''
  COMMENT '发布时间：2016/04/26',
  `new_model`              VARCHAR(32)       DEFAULT ''
  COMMENT '新型号:	22218',
  `old_model`              VARCHAR(32)       DEFAULT ''
  COMMENT '旧型号:	3518',
  `bearing_material`       VARCHAR(32)       DEFAULT ''
  COMMENT '轴承材料:	高温轴承钢',
  `inner_diameter`         VARCHAR(32)       DEFAULT ''
  COMMENT '内径（mm）:	90',
  `outer_diameter`         VARCHAR(32)       DEFAULT ''
  COMMENT '外径（mm）:	160',
  `weight`                 VARCHAR(32)       DEFAULT ''
  COMMENT '重量（kg）:	3.32',
  `width`                  VARCHAR(32)       DEFAULT ''
  COMMENT '宽度（mm）:	40',
  `cage_materials`         VARCHAR(32)       DEFAULT ''
  COMMENT '保持架及材料:',
  `use_text`               TEXT
  COMMENT '用途:',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '中国轴承产业服务平台 商品表';

### 搜轴网 品牌表
DROP TABLE IF EXISTS `bearing_soz_brand`;
CREATE TABLE `bearing_soz_brand` (
  `id`         INT(32)  NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify` DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `brand`      VARCHAR(32)       DEFAULT ''
  COMMENT '品牌：SKF',
  `url`        VARCHAR(32)       DEFAULT ''
  COMMENT '地址',
  `type`       VARCHAR(32)       DEFAULT ''
  COMMENT 'export、import',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '搜轴网 品牌表';

### 搜轴网 商品表
DROP TABLE IF EXISTS `bearing_soz_goods`;
CREATE TABLE `bearing_soz_goods` (
  `id`             INT(32)  NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`     DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`     DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `brand_id`       INT(32)
  COMMENT 'category_id',
  `model`          VARCHAR(32)
  COMMENT '型号',
  `brand`          VARCHAR(32)       DEFAULT ''
  COMMENT '品牌：SKF',
  `series`         VARCHAR(32)       DEFAULT ''
  COMMENT '系列：单列深沟球轴承',
  `inner_diameter` VARCHAR(32)       DEFAULT ''
  COMMENT '内径：3mm',
  `outer_diameter` VARCHAR(32)       DEFAULT ''
  COMMENT '外径：10mm',
  `width`         VARCHAR(32)       DEFAULT ''
  COMMENT '宽度：4mm',
  `images`         VARCHAR(256)      DEFAULT ''
  COMMENT '商品图片',
  `type`           VARCHAR(16)       DEFAULT ''
  COMMENT 'export国产、import进口',
  `detail_url`     VARCHAR(128)
  COMMENT '商品详情的URL',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '搜轴网 商品表';