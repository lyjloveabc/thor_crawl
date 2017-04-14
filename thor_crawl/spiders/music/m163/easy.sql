SELECT
  m163_playlist.main_id,
  m163_playlist.name,
  m163_playlist.subscribed_count,
  m163_playlist.tags,
  m163_playlist.description,
  m163_user.user_id,
  m163_user.nickname
FROM m163_playlist
  LEFT JOIN m163_user ON m163_playlist.creator_id = m163_user.user_id
ORDER BY subscribed_count DESC
LIMIT 10;

SELECT
  m163_playlist.name,
  m163_playlist.subscribed_count,
  m163_playlist.tags,
  m163_playlist.description,
  m163_user.user_id,
  m163_user.nickname,
  concat('http://music.163.com/#/playlist?id=', m163_playlist.main_id, '&userid=278673575&from=singlemessage') AS page_url
FROM m163_playlist
  LEFT JOIN m163_user ON m163_playlist.creator_id = m163_user.user_id
ORDER BY subscribed_count DESC
LIMIT 10;

SELECT
  m163_playlist.name,
  m163_playlist.subscribed_count,
  m163_playlist.tags,
  m163_user.nickname
  FROM m163_playlist
  LEFT JOIN m163_user ON m163_playlist.creator_id = m163_user.user_id
ORDER BY subscribed_count DESC
LIMIT 10;