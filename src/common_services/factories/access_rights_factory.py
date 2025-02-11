import factory

from projects.models import AccessRights


class AccessRightsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessRights

    access_rights_name = factory.Iterator(
        ["admin", "viewer", "creator", "editor", "deleter"]
    )
    description = factory.Faker("sentence")
    tag = factory.Iterator(
        [
            AccessRights.TagsChoices.ADMIN,
            AccessRights.TagsChoices.VIEWER,
            AccessRights.TagsChoices.CREATOR,
            AccessRights.TagsChoices.EDITOR,
            AccessRights.TagsChoices.DELETER,
        ]
    )
