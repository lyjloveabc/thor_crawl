### 网易云音乐 歌曲表
DROP TABLE IF EXISTS `m163_song`;
CREATE TABLE `m163_song` (
  `id`                   INT           NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`           DATETIME      NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`           DATETIME      NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `m163_id`              INT           NOT NULL
  COMMENT '163的歌曲ID',

  `name`                 VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '歌曲名称',

  `position`             TINYINT       NOT NULL DEFAULT 1
  COMMENT '位置',

  `alias`                VARCHAR(1024) NOT NULL DEFAULT ''
  COMMENT '歌曲别称',

  `status`               TINYINT       NOT NULL DEFAULT 0
  COMMENT '状态',

  `fee`                  VARCHAR(8)    NOT NULL DEFAULT '0'
  COMMENT '状态',

  `copyright_id`         INT           NOT NULL DEFAULT 0
  COMMENT '状态',

  `disc`                 VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `no`                   INT           NOT NULL DEFAULT 0
  COMMENT '',

  `starred`              BOOLEAN       NOT NULL DEFAULT FALSE
  COMMENT '',

  `popularity`           INT           NOT NULL DEFAULT 0
  COMMENT '流行度',

  `score`                INT           NOT NULL DEFAULT 0
  COMMENT '分数',

  `starred_num`          INT           NOT NULL DEFAULT 0
  COMMENT '',

  `duration`             INT           NOT NULL DEFAULT 0
  COMMENT '音长',

  `played_num`           INT           NOT NULL DEFAULT 0
  COMMENT '',

  `day_plays`            INT           NOT NULL DEFAULT 0
  COMMENT '',

  `hear_time`            INT           NOT NULL DEFAULT 0
  COMMENT '',

  `ring_tone`            VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `crbt`                 VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `audition`             VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `copy_from`            VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `comment_thread_id`    VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `rt_url`               VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '',

  `f_type`               TINYINT       NOT NULL DEFAULT 0
  COMMENT '',

  `rt_urls`              VARCHAR(256)  NOT NULL DEFAULT ''
  COMMENT '',

  `copyright`            INT           NOT NULL DEFAULT 0
  COMMENT '版权',

  `mv_id`                INT           NOT NULL DEFAULT 0
  COMMENT 'mvID',

  `mp3_url`              VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT 'lMusic mp3 url',

  `rtype`                TINYINT       NOT NULL DEFAULT 0
  COMMENT 'lMusic mp3 url',

  `r_url`                VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT 'lMusic mp3 url',

  `artist_ids`           VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT 'artists 中的 artist 的ID',

  `first_artist_id`      INT           NOT NULL DEFAULT 0
  COMMENT '艺术家ID',

  `first_artist_name`    VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '艺术家名称',

  `first_artist_pic_url` VARCHAR(128)  NOT NULL DEFAULT ''
  COMMENT '艺术家照片',

  `album_id`             INT           NOT NULL DEFAULT 0
  COMMENT '专辑ID',

  `b_music_id`           INT           NOT NULL DEFAULT 0
  COMMENT 'b_music_id',

  `h_music_id`           INT           NOT NULL DEFAULT 0
  COMMENT 'h_music_id',

  `m_music_id`           INT           NOT NULL DEFAULT 0
  COMMENT 'm_music_id',

  `l_music_id`           INT           NOT NULL DEFAULT 0
  COMMENT 'l_music_id',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_m163_user_id`(m163_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '用户表';

### 网易云音乐 歌单音乐等级表
DROP TABLE IF EXISTS `m163_music_level`;
CREATE TABLE `m163_music_level` (
  `id`             INT(16)      NOT NULL  AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`     DATETIME     NOT NULL  DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`     DATETIME     NOT NULL  DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `music_level_id` INT          NOT NULL
  COMMENT 'music_level_id',

  `name`           VARCHAR(128) NOT NULL  DEFAULT ''
  COMMENT 'music_level_id',

  `size`           INT          NOT NULL  DEFAULT 1
  COMMENT '大小',

  `extension`      VARCHAR(16)  NOT NULL  DEFAULT ''
  COMMENT '扩展名',

  `sr`             VARCHAR(16)  NOT NULL  DEFAULT ''
  COMMENT '',

  `dfs_id`         INT          NOT NULL  DEFAULT 0
  COMMENT '关键ID',

  `bitrate`        VARCHAR(16)  NOT NULL  DEFAULT ''
  COMMENT '',

  `play_time`      VARCHAR(16)  NOT NULL  DEFAULT ''
  COMMENT '',

  `volume_delta`   VARCHAR(16)  NOT NULL  DEFAULT ''
  COMMENT '',
  `dfs_id_str`     VARCHAR(32)  NOT NULL  DEFAULT ''
  COMMENT '',

  `music_level`    VARCHAR(16)  NOT NULL  DEFAULT ''
  COMMENT '音乐等级',

  `m163_song_id`   INT          NOT NULL  DEFAULT 0
  COMMENT '',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_m163_user_id`(music_level_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '用户表';

### 网易云音乐 歌单歌曲关系表
DROP TABLE IF EXISTS `m163_playlist_x_song`;
CREATE TABLE `m163_playlist_x_song` (
  `id`               INT(16)  NOT NULL AUTO_INCREMENT
  COMMENT '数据库自增ID',
  `gmt_create`       DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据创建时间',
  `gmt_modify`       DATETIME NOT NULL DEFAULT '1970-01-01 00:00:01'
  COMMENT '数据修改时间',

  `m163_playlist_id` INT      NOT NULL
  COMMENT '歌单ID',

  `m163_song_id`     INT      NOT NULL
  COMMENT '歌曲ID',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_m163_user_id`(m163_playlist_id, m163_song_id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COMMENT = '用户表';