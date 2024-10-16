from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_initial_categories(sender, **kwargs):
    categories = ['食費', '日用品', '交通費', '娯楽', '美容・衣服', '医療・保険', '通信', '住まい', '給与', 'ボーナス', 'その他収入']
    for category in categories:
        Category.objects.get_or_create(name=category)