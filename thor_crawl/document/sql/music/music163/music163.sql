### 网易云音乐 歌单表
DROP TABLE IF EXISTS `m163_playlist`;
CREATE TABLE `m163_playlist` (
  `id`                       INT(16)       NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`               DATETIME      NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`               DATETIME      NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `main_id`                  INT(16)       NOT NULL
  COMMENT '主ID，歌单ID',

  `name`                     VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '歌单名称',

  `track_number_update_time` VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '',

  `status`                   TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `user_id`                  INT(16)       NOT NULL DEFAULT 0
  COMMENT '用户ID',

  `create_time`              VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '创建时间',

  `update_time`              VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '更新时间',

  `subscribed_count`         INT(16)       NOT NULL DEFAULT 0
  COMMENT '被收藏数量',

  `track_count`              INT(16)       NOT NULL DEFAULT 0
  COMMENT '歌单中歌曲数量',

  `cloud_track_count`        INT(16)       NOT NULL DEFAULT 0
  COMMENT '',

  `cover_img_url`            VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '封面图片',

  `cover_img_id`             VARCHAR(32)   NOT NULL DEFAULT 0
  COMMENT '封面图片ID',

  `description`              VARCHAR(1024) NOT NULL DEFAULT ''
  COMMENT '描述',

  `tags`                     VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '标签，用英文逗号分隔',

  `play_count`               INT(16)       NOT NULL DEFAULT 0
  COMMENT '收听数',

  `track_update_time`        VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '',

  `special_type`             TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `total_duration`           VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '',

  `tracks`                   VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '',

  `subscribed`               VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '',

  `comment_thread_id`        VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '',

  `new_imported`             BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '',

  `ad_type`                  TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `high_quality`             BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '',

  `privacy`                  TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `ordered`                  BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '',

  `anonimous`                BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '',

  `share_count`              INT(16)       NOT NULL DEFAULT 0
  COMMENT '分享数',

  `cover_img_id__str`        VARCHAR(32)   NOT NULL DEFAULT 0
  COMMENT '封面图片ID字符串',

  `comment_count`            INT(16)       NOT NULL DEFAULT 0
  COMMENT '评论数',

  `creator_id`               INT(16)       NOT NULL DEFAULT 0
  COMMENT '创建者的用户ID',

  `subscriber_id`            INT(16)       NOT NULL DEFAULT 0
  COMMENT '其中一个订阅者的用户ID',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_m163_playlist_id`(main_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '歌单表 m163_playlist';

### 网易云音乐 用户表
DROP TABLE IF EXISTS `m163_user`;
CREATE TABLE `m163_user` (
  `id`                    INT(16)       NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`            DATETIME      NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`            DATETIME      NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `default_avatar`        BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '主ID，歌单ID',

  `province`              VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '省会编号',

  `auth_status`           TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `followed`              BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '',

  `avatar_url`            VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '用户头像地址',

  `account_status`        TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `gender`                SMALLINT      NOT NULL DEFAULT 0
  COMMENT '',

  `city`                  VARCHAR(16)   NOT NULL DEFAULT ''
  COMMENT '城市编号',

  `birthday`              VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '生日',

  `user_id`               INT(16)       NOT NULL DEFAULT 0
  COMMENT '网易的用户ID',

  `user_type`             TINYINT       NOT NULL DEFAULT 0
  COMMENT '网易的用户类型',

  `nickname`              VARCHAR(32)   NOT NULL DEFAULT 0
  COMMENT '用户昵称',

  `signature`             VARCHAR(256)  NOT NULL DEFAULT ''
  COMMENT '个人介绍',

  `description`           VARCHAR(1024) NOT NULL DEFAULT ''
  COMMENT '描述',

  `detail_description`    VARCHAR(1024) NOT NULL DEFAULT ''
  COMMENT '细节描述',

  `avatar_img_id`         VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '',

  `background_img_id`     VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '',

  `background_url`        VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `authority`             SMALLINT      NOT NULL DEFAULT 0
  COMMENT '',

  `mutual`                SMALLINT      NOT NULL DEFAULT 0
  COMMENT '',

  `expert_tags`           VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '音乐达人标签',

  `dj_status`             TINYINT       NOT NULL DEFAULT 0
  COMMENT '网易的用户类型',

  `vip_type`              TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `remark_name`           VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `avatar_img_id_str`     VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '',

  `background_img_id_str` VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '',

  `avatar_img_id__str`    VARCHAR(32)   NOT NULL DEFAULT ''
  COMMENT '',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_m163_user_id`(user_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '用户表 m163_user';