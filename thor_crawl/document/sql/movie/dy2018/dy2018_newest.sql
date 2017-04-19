### 电影天堂 最新电影表
DROP TABLE IF EXISTS `dy2018_newest`;
CREATE TABLE `dy2018_newest` (
  `id`          INT         NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`  DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`  DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `dy2018_id`   INT         NOT NULL
  COMMENT '电影天堂的ID',

  `name`        VARCHAR(64) NOT NULL
  COMMENT '电影名称',

  `publish_day` VARCHAR(16) NOT NULL
  COMMENT '发布日期',

  `click_count` INT         NOT NULL DEFAULT 0
  COMMENT '点击数量',

  `detail_url`  VARCHAR(128) NOT NULL
  COMMENT '详情地址',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_dy2018_id`(dy2018_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '电影天堂 最新电影表';