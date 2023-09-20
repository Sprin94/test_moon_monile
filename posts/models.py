from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        db_column="user_id",
        null=False,
    )
    wall_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wall_posts',
        verbose_name='Владелец стены',
        db_column="wall_owner_id",
        null=False,
    )
    title = models.CharField('Заголовок', max_length=100, null=False)
    content = models.TextField('Текст поста', null=False)
    created_at = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
        editable=False
    )

    def __str__(self) -> str:
        return self.content[:15]

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
