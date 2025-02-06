import factory

from projects.models import Permission


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission

    permission_name = factory.Iterator(
        ["admin", "viewer", "creator", "editor", "deleter"]
    )
    description = factory.Faker("sentence")
    tag = factory.Iterator(
        [
            Permission.TagsChoices.ADMIN,
            Permission.TagsChoices.VIEWER,
            Permission.TagsChoices.CREATOR,
            Permission.TagsChoices.EDITOR,
            Permission.TagsChoices.DELETER,
        ]
    )
