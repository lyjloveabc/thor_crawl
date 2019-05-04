UPDATE fang_city_zone_new
SET
  property_fee = replace(property_fee, '。月', '·月')
WHERE property_fee LIKE '%。月%';
UPDATE fang_city_zone_new
SET
  property_fee = replace(property_fee, '元/?O?月', '元/平方米')
WHERE property_fee LIKE '%元/?O?月%';

# 统计小区数量
SELECT
  city_name     AS '城市名称',
  province_name AS '所属省份',
  num           AS '小区数量'
FROM fang_city_zone_num
ORDER BY province_name, city_name;

# 统计有占地面积的小区个数
SELECT count(*)
FROM fang_city_zone_new
WHERE land_area != '' AND land_area IS NOT NULL;

# 统计占地面积
SELECT
  city_name                                          AS '城市名称',
  province_name                                      AS '所属省份',
  sum(cast(replace(land_area, '平方米', '') AS SIGNED)) AS '面积之和'
FROM fang_city_zone_new
WHERE land_area != '' AND land_area IS NOT NULL
GROUP BY province_name, city_name;

# 统计有建筑面积的小区个数
SELECT count(*)
FROM fang_city_zone_new
WHERE building_area != '' AND building_area IS NOT NULL;

# 统计建筑面积
SELECT
  city_name                                              AS '城市名称',
  province_name                                          AS '所属省份',
  sum(cast(replace(building_area, '平方米', '') AS SIGNED)) AS '面积之和'
FROM fang_city_zone_new
WHERE building_area != '' AND building_area IS NOT NULL
GROUP BY province_name, city_name;

# 统计有物业费单价的小区个数
SELECT count(*)
FROM fang_city_zone_new
WHERE property_fee != '' AND property_fee IS NOT NULL;

# 统计物业费单价
SELECT
  city_name                                                         AS '城市名称',
  province_name                                                     AS '所属省份',
  count(*)                                                          AS '小区数量',
  sum(cast(replace(
               replace(
                   replace(
                       replace(
                           replace(property_fee, '元/㎡·月', ''),
                           '元/平方米·月',
                           ''
                       ),
                       '元/平米·月',
                       ''
                   ),
                   '元/平方米',
                   ''
               ),
               '/月',
               ''
           ) AS DECIMAL(10, 2)))                                    AS '物业费之和',
  cast(sum(cast(replace(
                    replace(
                        replace(
                            replace(
                                replace(property_fee, '元/㎡·月', ''),
                                '元/平方米·月',
                                ''
                            ),
                            '元/平米·月',
                            ''
                        ),
                        '元/平方米',
                        ''
                    ),
                    '/月',
                    ''
                ) AS DECIMAL(10, 2))) / count(*) AS DECIMAL(10, 2)) AS '物业费平均'
FROM fang_city_zone_new
WHERE property_fee != '' AND property_fee IS NOT NULL
      AND property_fee NOT LIKE '%元/户·月' AND property_fee NOT LIKE '%·天' AND property_fee NOT LIKE '%元/户/月'
#       AND cast(replace(
#                    replace(
#                        replace(
#                            replace(
#                                replace(property_fee, '元/㎡·月', ''),
#                                '元/平方米·月',
#                                ''
#                            ),
#                            '元/平米·月',
#                            ''
#                        ),
#                        '元/平方米',
#                        ''
#                    ),
#                    '/月',
#                    ''
#                ) AS DECIMAL(10, 2)) <= 40
GROUP BY province_name, city_name;

SELECT DISTINCT cast(replace(
                         replace(
                             replace(
                                 replace(
                                     replace(property_fee, '元/㎡·月', ''),
                                     '元/平方米·月',
                                     ''
                                 ),
                                 '元/平米·月',
                                 ''
                             ),
                             '元/平方米',
                             ''
                         ),
                         '/月',
                         ''

                     ) AS DECIMAL(10, 2)) AS pf
FROM fang_city_zone_new
WHERE property_fee != '' AND property_fee IS NOT NULL
      AND property_fee NOT LIKE '%元/户·月' AND property_fee NOT LIKE '%·天' AND property_fee NOT LIKE '%元/户/月'
ORDER BY pf;

### 分开处理
SELECT
  id,
  url,
  detail_url
FROM fang_city_zone_new
WHERE id >= 180001 AND url != '' AND url IS NOT NULL AND url NOT LIKE '/house-xm%'
LIMIT 0, 2000;

