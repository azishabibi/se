# Generated by Django 4.2.5 on 2023-11-30 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "post_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="帖子id"
                    ),
                ),
                (
                    "user_id",
                    models.CharField(max_length=50, null=True, verbose_name="发帖用户id"),
                ),
                (
                    "publish_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="发布时间"),
                ),
                ("title", models.CharField(max_length=50, verbose_name="帖子标题")),
                (
                    "content",
                    models.CharField(max_length=5000, null=True, verbose_name="帖子文字内容"),
                ),
                (
                    "picture_1",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片1"),
                ),
                (
                    "picture_2",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片2"),
                ),
                (
                    "picture_3",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片3"),
                ),
                (
                    "picture_4",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片4"),
                ),
                (
                    "picture_5",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片5"),
                ),
                (
                    "picture_6",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片6"),
                ),
                (
                    "picture_7",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片7"),
                ),
                (
                    "picture_8",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片8"),
                ),
                (
                    "picture_9",
                    models.ImageField(null=True, upload_to="", verbose_name="帖子图片9"),
                ),
                (
                    "comment_counts",
                    models.IntegerField(default=0, verbose_name="话题评论数"),
                ),
                ("click_counts", models.IntegerField(default=0, verbose_name="话题点击数")),
                ("like_counts", models.IntegerField(default=0, verbose_name="点赞数")),
                ("is_top", models.BooleanField(default=False, verbose_name="是否置顶")),
            ],
            options={"verbose_name": "话题", "verbose_name_plural": "话题",},
        ),
    ]
