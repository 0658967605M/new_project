from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    roles = {
        'Reader': ['view_article'],
        'Publisher':
        ['add_article', 'view_article', 'change_article', 'delete_article'],
        'Editor': ['view_article', 'change_article', 'delete_article'],
    }

    for role, perms in roles.items():
        group, _ = Group.objects.get_or_create(name=role)
        permissions = Permission.objects.filter(codename__in=perms)
        group.permissions.set(permissions)
