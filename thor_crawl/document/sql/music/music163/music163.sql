### 网易云音乐 歌单表
DROP TABLE IF EXISTS `m163_playlist`;
CREATE TABLE `m163_playlist` (
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

  `track_number_update_time` VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '',

  `status`                   TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `user_id`                  INT(16)      NOT NULL DEFAULT 0
  COMMENT '用户ID',

  `create_time`              VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '创建时间',

  `update_time`              VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '更新时间',

  `subscribed_count`         INT(16)      NOT NULL DEFAULT 0
  COMMENT '被收藏数量',

  `track_count`              INT(16)      NOT NULL DEFAULT 0
  COMMENT '歌单中歌曲数量',

  `cloud_track_count`        INT(16)      NOT NULL DEFAULT 0
  COMMENT '',

  `cover_img_url`            VARCHAR(128) NOT NULL DEFAULT ''
  COMMENT '封面图片',

  `cover_img_id`             VARCHAR(32)  NOT NULL DEFAULT 0
  COMMENT '封面图片ID',

  `description`              VARCHAR(512) NOT NULL DEFAULT ''
  COMMENT '描述',

  `tags`                     VARCHAR(64)  NOT NULL DEFAULT ''
  COMMENT '标签，用英文逗号分隔',

  `play_count`               INT(16)      NOT NULL DEFAULT 0
  COMMENT '收听数',

  `track_update_time`        VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '',

  `special_type`             TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `total_duration`           TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `tracks`                   VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '',

  `subscribed`               VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '',

  `comment_thread_id`        VARCHAR(32)  NOT NULL DEFAULT ''
  COMMENT '',

  `new_imported`             BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `ad_type`                  TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `high_quality`             BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `privacy`                  TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `ordered`                  BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `anonimous`                BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `share_count`              INT(16)      NOT NULL DEFAULT 0
  COMMENT '分享数',

  `cover_img_id_str`         VARCHAR(32)  NOT NULL DEFAULT 0
  COMMENT '封面图片ID字符串',

  `comment_count`            INT(16)      NOT NULL DEFAULT 0
  COMMENT '评论数',

  `creator_id`               INT(16)      NOT NULL DEFAULT 0
  COMMENT '创建者的用户ID',

  `subscriber_id`            INT(16)      NOT NULL DEFAULT 0
  COMMENT '其中一个订阅者的用户ID',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '歌单表 m163_playlist';

### 网易云音乐 用户表
DROP TABLE IF EXISTS `m163_user`;
CREATE TABLE `m163_user` (
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

  `cover_img_id`             VARCHAR(16)  NOT NULL DEFAULT 0
  COMMENT '封面图片ID',

  `description`              VARCHAR(512) NOT NULL DEFAULT ''
  COMMENT '描述',

  `tags`                     VARCHAR(64)  NOT NULL DEFAULT ''
  COMMENT '标签，用英文逗号分隔',

  `play_count`               INT(16)      NOT NULL DEFAULT 0
  COMMENT '收听数',

  `track_update_time`        INT(16)      NOT NULL DEFAULT 0
  COMMENT '',

  `special_type`             TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `total_duration`           TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `tracks`                   VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '',

  `subscribed`               VARCHAR(16)  NOT NULL DEFAULT ''
  COMMENT '',

  `comment_thread_id`        VARCHAR(32)  NOT NULL DEFAULT ''
  COMMENT '',

  `new_imported`             BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `ad_type`                  TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `high_quality`             BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `privacy`                  TINYINT      NOT NULL DEFAULT 0
  COMMENT '',

  `ordered`                  BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `anonimous`                BOOLEAN      NOT NULL DEFAULT FALSE
  COMMENT '',

  `share_count`              INT(16)      NOT NULL DEFAULT 0
  COMMENT '分享数',

  `cover_img_id_str`         VARCHAR(16)  NOT NULL DEFAULT 0
  COMMENT '封面图片ID字符串',

  `comment_count`            INT(16)      NOT NULL DEFAULT 0
  COMMENT '评论数',

  `creator_id`               INT(16)      NOT NULL
  COMMENT '创建者的用户ID',

  `subscriber_id`            INT(16)      NOT NULL DEFAULT 0
  COMMENT '其中一个订阅者的用户ID',

  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '用户表 m163_user';