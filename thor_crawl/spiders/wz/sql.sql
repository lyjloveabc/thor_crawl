CREATE TABLE `wz_zb`
(
    `id`              BIGINT       NOT NULL AUTO_INCREMENT COMMENT '数据库自增ID',
    `create_time`     DATETIME     NOT NULL                             DEFAULT CURRENT_TIMESTAMP COMMENT '数据创建时间',
    `modify_time`     DATETIME     NOT NULL ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '数据修改时间',
    `t_id`            BIGINT       NOT NULL COMMENT '视频ID',
    `c_id`            BIGINT       NOT NULL COMMENT '用户ID',
    `zb_id`           BIGINT       NOT NULL COMMENT '直播间ID',
    `title`           VARCHAR(100) NOT NULL COMMENT '标题',
    `start_time`      DATETIME     NOT NULL COMMENT '开始时间',
    `add_time`        VARCHAR(200) NOT NULL COMMENT '添加时间',
    `cover`           VARCHAR(200)     NOT NULL COMMENT '图片',
    `tv_url`          varchar(200) NOT NULL COMMENT '直播url',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`tv_url`)
)
    COMMENT ='微赞-直播'
    COLLATE = 'utf8mb4_general_ci'
    ENGINE = InnoDB;
