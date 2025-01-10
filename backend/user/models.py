from django.db import models


class Users(models.Model):
    userId = models.AutoField(primary_key=True, verbose_name="User ID")
    name = models.CharField(max_length=50, verbose_name="Name")
    email = models.CharField(max_length=100, verbose_name="Email", null=True, blank=True)
    password = models.CharField(max_length=50, verbose_name="Password")
    status = models.CharField(max_length=50, choices=(
        ('User', 'User'),
        ('Administrator', 'Administrator'),
        ('Root', 'Root')
    ), default='User', verbose_name="Status")
    avatar = models.CharField(max_length=250, default='https://s2.loli.net/2024/12/08/MeOiLyYdNt7wK5E.png')
    profile = models.CharField(max_length=200, blank=True, null=True, verbose_name="Profile")
    coin = models.IntegerField(default=0, verbose_name="Coin Quantity")
    color = models.BooleanField(default=False, verbose_name="Color Preference (0: Dark Mode, 1: Background Grain)")
    token = models.CharField(max_length=500, blank=True, null=True, verbose_name="Token")
    block = models.BooleanField(default=False, verbose_name="Block")
    date = models.DateTimeField(auto_now_add=True)


class Messages(models.Model):
    messageId = models.AutoField(primary_key=True, verbose_name='消息ID')
    userId = models.IntegerField(verbose_name='用户ID', db_column='UserId')
    type = models.CharField(max_length=50,
                            choices=[('Notice', '公告'), ('Comment', '评论'), ('Reply', '回复'), ('Answer', '回答'),
                                     ('Reward', '奖励')], verbose_name='类型')
    read = models.BooleanField(default=False, verbose_name='是否已读')


class NoticeMessages(models.Model):
    messageId = models.IntegerField(default=0)
    noticeId = models.IntegerField(null=True, blank=True, verbose_name='公告ID')


class ShareMessages(models.Model):
    messageId = models.IntegerField(default=0)
    shareId = models.IntegerField(null=True, blank=True, verbose_name='分享ID')


class RewardMessages(models.Model):
    messageId = models.IntegerField(default=0)
    rewardId = models.IntegerField(null=True, blank=True, verbose_name='分享ID')


class Follows(models.Model):
    followId = models.AutoField(primary_key=True)  # PK, 关注时唯一指定
    fromId = models.IntegerField(default=0)  # FK, 关联到 Users, 关注者的 id
    toId = models.IntegerField(default=0)  # FK, 关联到 Users, 被关注者的 id
    date = models.DateTimeField(auto_now_add=True)  # 关注时间


class Tags(models.Model):
    tagId = models.AutoField(primary_key=True)  # PK, 标签创建时唯一指定
    name = models.CharField(max_length=50)  # 标签名


class Notices(models.Model):
    noticeId = models.AutoField(primary_key=True)  # PK, 公告创建时唯一指定
    title = models.CharField(max_length=50)
    text = models.TextField()  # 公告内容
    date = models.DateTimeField(auto_now_add=True)  # 创建时间
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name="URL")


class NoticeTags(models.Model):
    noticeTagId = models.AutoField(primary_key=True)  # PK, 创建公告时唯一指定
    noticeId = models.IntegerField(default=0)  # FK，关联到 Notices，帖子 id
    tagId = models.IntegerField(default=0)  # FK, 关联到 Tags, 标签 id


class Shares(models.Model):
    shareId = models.AutoField(primary_key=True)  # 分享ID，自增长
    headline = models.CharField(max_length=50)  # 标题
    price = models.IntegerField(default=0)  # 价格，默认为0
    creatorId = models.IntegerField(default=0)  # 创建者id，外键关联到用户表
    text = models.TextField()  # 文章内容
    cover = models.CharField(max_length=255)  # 封面路径
    profile = models.CharField(max_length=200)  # 简介
    resourceLink = models.CharField(max_length=255)  # 资源路径
    like = models.IntegerField(default=0)  # 点赞数量，默认为0
    dislike = models.IntegerField(default=0)  # 点踩数量，默认为0
    coin = models.IntegerField(default=0)  # 菜币数量，默认为0 # 目前api已经无用
    favourite = models.IntegerField(default=0)  # 收藏数量，默认为0
    date = models.DateTimeField(auto_now_add=True)
    bhpanUrl = models.CharField(max_length=255, blank=True, null=True, verbose_name="BHPAN URL")
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name="URL")
    vector = models.BinaryField(null=True, blank=True)


class ShareTags(models.Model):
    shareTagId = models.AutoField(primary_key=True)  # PK, 创建共享帖子时唯一指定
    shareId = models.IntegerField(default=0)  # FK，关联到 Shares，帖子 id
    creatorId = models.IntegerField(default=0)  # FK, 关联到 Users, 创建者 id
    tagId = models.IntegerField(default=0)  # FK, 关联到 Tags, 标签 id


# 定义操作员模型
class ShareOperators(models.Model):
    operatorId = models.AutoField(primary_key=True)  # PK, 进行操作时唯一指定
    shareId = models.IntegerField(default=0)  # FK, 关联到 Shares
    userId = models.IntegerField(default=0)  # FK, 关联到 Users
    type = models.CharField(max_length=50,
                            choices=[('Purchase', '购买'), ('Like', '点赞'), ('Dislike', '点踩'), ('Coin', '投币'),
                                     ('Favourite', '收藏')])
    coin = models.IntegerField(null=True, blank=True)  # 投币数量，仅 Type 为 Coin 时有效
    date = models.DateTimeField(auto_now_add=True)  # 操作时间


class Comments(models.Model):
    commentId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, choices=[('Comment', '回复帖子'), ('Reply', '回复回复')],
                            verbose_name='仅有两种值：Comment，Reply（回复帖子、回复回复）')
    shareId = models.IntegerField(default=0)
    replyId = models.IntegerField(default=0)  # Comment
    creatorId = models.IntegerField(default=0)
    text = models.TextField(verbose_name='回复正文')
    date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class CommentOperators(models.Model):
    commentOperatorId = models.AutoField(primary_key=True)
    commentId = models.IntegerField(default=0)
    userId = models.IntegerField(default=0)
    type = models.CharField(max_length=50, choices=[('Like', 'Like'), ('Dislike', 'Dislike')])
    date = models.DateTimeField(auto_now_add=True)


class Rewards(models.Model):
    rewardId = models.AutoField(primary_key=True)  # PK, 创建互助贴时唯一指定
    headline = models.CharField(max_length=50)  # 标题
    reward = models.IntegerField()  # 悬赏金额
    creatorId = models.IntegerField(default=0)  # FK, 关联到 Users, 创建者 id
    text = models.TextField()  # 文章内容
    cover = models.CharField(max_length=255)  # 封面路径
    profile = models.CharField(max_length=200)  # 简介
    date = models.DateTimeField(auto_now_add=True)  # 创建时间
    close = models.BooleanField(default=False, verbose_name='是否关闭')
    answerId = models.IntegerField(default=0)  # 最终答案
    url = models.CharField(max_length=255, blank=True, null=True, verbose_name="URL")


class RewardTags(models.Model):
    rewardTagId = models.AutoField(primary_key=True)  # PK, 创建互助帖子标签时唯一指定
    rewardId = models.IntegerField(default=0)  # FK, 关联到 Rewards, 帖子 id
    tagId = models.IntegerField(default=0)  # FK, 关联到 Tags, 标签 id


class Answers(models.Model):
    answerId = models.AutoField(primary_key=True)  # PK, 互助评论创建时唯一指定
    rewardId = models.IntegerField(default=0)  # FK, 关联到 Rewards, 共享标签 id
    creatorId = models.IntegerField(default=0)  # FK, 关联到 Users, 创建者 id
    text = models.TextField()  # 回复正文
    resource_link = models.CharField(max_length=255)  # 资源链接
    date = models.DateTimeField(auto_now_add=True)  # 评论时间
