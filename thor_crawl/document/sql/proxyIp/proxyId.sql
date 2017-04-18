### 代理IP表
DROP TABLE IF EXISTS `proxy_ip`;
CREATE TABLE `proxy_ip` (
  `id`            INT(16)     NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`    DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`    DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `ip`            VARCHAR(16) NOT NULL
  COMMENT 'ip: 119.39.112.115',

  `port`          VARCHAR(8)  NOT NULL DEFAULT '80'
  COMMENT '端口: 8081',

  `address`       VARCHAR(64) NOT NULL DEFAULT ''
  COMMENT '代理ip位置: 湖南省长沙市',

  `type`          CHAR(1)     NOT NULL DEFAULT '1'
  COMMENT '代理类型: 1高匿代理',

  `ip_type`       VARCHAR(8)  NOT NULL DEFAULT 'http'
  COMMENT '代理IP类型: http、https',

  `check_time`    VARCHAR(64) NOT NULL DEFAULT ''
  COMMENT '验证时间: 时间字符串',

  `survival_time` VARCHAR(32) NOT NULL DEFAULT ''
  COMMENT '存活时间: 98天',

  `operator`      CHAR(1)     NOT NULL DEFAULT ''
  COMMENT '运营商: 1电信，2移动，3联通',

  `source`        VARCHAR(16) NOT NULL DEFAULT ''
  COMMENT '来源网站名称',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_m163_user_id`(m163_playlist_id, m163_song_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = 'proxy_ip';