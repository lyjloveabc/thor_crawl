SELECT
  city_name     AS '城市名称',
  province_name AS '所属',
  num           AS '小区数量'
FROM fang_city_zone_num
ORDER BY province_name, city_name;
