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
WHERE building_area != '' AND building_area IS NOT NULL;

# 统计物业费单价
SELECT
  city_name                                              AS '城市名称',
  province_name                                          AS '所属省份',
  sum(cast(replace(building_area, '平方米', '') AS SIGNED)) AS '面积之和'
FROM fang_city_zone_new
WHERE building_area != '' AND building_area IS NOT NULL
GROUP BY province_name, city_name;

### 分开处理
SELECT
  id,
  url,
  detail_url
FROM fang_city_zone_new
WHERE id >= 180001 AND url != '' AND url IS NOT NULL AND url NOT LIKE '/house-xm%'
LIMIT 0, 2000;

