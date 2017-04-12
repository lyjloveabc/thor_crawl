### 网易云音乐 歌单表
DROP TABLE IF EXISTS `playlist`;
CREATE TABLE `playlist` (
  `id`                       INT(16)      NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`               DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`               DATETIME     NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `main_id`                  INT(16)      NOT NULL
  COMMENT '主ID，歌单ID',

  `name`                     VARCHAR(128) NOT NULL DEFAULT ''
  COMMENT '歌单名称',

  `track_number_update_time` INT(16)      NOT NULL DEFAULT 0
  COMMENT '',

  `status`                   TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `user_id`                  INT(16)      NOT NULL DEFAULT 0
  COMMENT '用户ID',

  `create_time`              INT(16)      NOT NULL DEFAULT 0
  COMMENT '创建时间',

  `update_time`              INT(16)      NOT NULL DEFAULT 0
  COMMENT '更新时间',

  `subscribed_count`         INT(16)      NOT NULL DEFAULT 0
  COMMENT '被收藏数量',

  `track_count`              INT(16)      NOT NULL DEFAULT 0
  COMMENT '歌单中歌曲数量',

  `cloud_track_count`        INT(16)      NOT NULL DEFAULT 0
  COMMENT '',

  `cover_img_url`            VARCHAR(128) NOT NULL DEFAULT ''
  COMMENT '封面图片',

  `cover_img_id`             INT(16)      NOT NULL DEFAULT 0
  COMMENT '封面图片ID',

  `description`              VARCHAR(512) NOT NULL DEFAULT ''
  COMMENT '描述',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '歌单表 playlist';