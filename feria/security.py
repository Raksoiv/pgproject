from django.db.models import Q

import feria.models as models


def user_forum(request, forum_id):
    f = models.Forum.objects.filter(id=forum_id)
    f = f.filter(
        Q(team__in=request.user.team_set.all())
        | Q(public=True))
    return True if f else False


def user_team(request, team_id):
    if request.user.team_set.filter(pk=team_id):
        return True

    return False


def user_epic(request, epic_id):
    epic = models.Epic.objects.get(pk=epic_id)
    if models.Team.objects.filter(user=request.user, epic=epic):
        return True

    return False


def user_feature(request, feature_id):
    feature = models.Feature.objects.get(pk=feature_id)
    if models.Team.objects.filter(user=request.user, epic=feature.epic):
        return True

    return False
