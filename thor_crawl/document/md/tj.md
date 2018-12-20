    SELECT
      area_name,
      count(*) AS c
    FROM sou_fang_renting
    GROUP BY area_name
    ORDER BY c DESC;