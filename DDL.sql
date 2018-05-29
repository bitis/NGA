create database nga;

create table subjects
(
  id           int primary key auto_increment,
  tid          int comment '帖子id',
  fid          int comment '板块id',
  authorid     int comment '作者id',
  subject      varchar(255) comment '帖子标题',
  postdate     int comment '发帖时间',
  lastpost     int comment '最后回复时间',
  replies      int comment '回复数量',
  forumname    varchar(255) comment '板块名字',
  found_news   boolean         default false
  comment '是否需要更新内容',
  comment_page int             default 1
  comment '当前已经记录到第几页(下次从此处开始)'
)
  comment '主题';

create table comments
(
  id                int primary key auto_increment,
  pid               int comment '评论id',
  fid               int comment '板块id',
  tid               int comment '帖子id',
  postdate          datetime comment '评论时间',
  content           text comment '评论内容',
  from_client       varchar(255) comment '使用设备',
  lou               int comment '楼层',
  postdatetimestamp int comment '发表评论时间戳',
  comment_to_id     int comment '被评论的评论id',
  vote_good         int comment '被点赞数量',
  vote_bad          int comment '被点踩数量',
  authorid          int comment '作者id',
  reputation        varchar(255) comment 'unknow',
  is_user_quote     int comment '是否是引用',
  isTieTiao         int comment '是否是贴条'
)
  comment '评论';