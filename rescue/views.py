from wsgiref.util import FileWrapper

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.http import HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import render

from rescue.models import ProjectRole
from pathlib import Path

EXPORT = Path.cwd()/"export"

def articles_file(project: int) -> Path:
    return EXPORT / "articles" / f"project_{project}.tgz"


def add_suffix(size: int) -> str:
    if size > 1E9:
        size = round(size/1E9)
        suffix = "GB"
    elif size > 1E6:
        size = round(size/1E6)
        suffix = "MB"
    elif size > 1E3:
        size = round(size/1E3)
        suffix = "kB"
    else:
        suffix = "B"
    return f"{size}{suffix}"


@login_required
def index(request):
    projects = [pr.project for pr in ProjectRole.objects.filter(user=request.user, role__label='admin').order_by("project__pk")]
    for p in projects:
        articles = articles_file(p.pk)
        p.has_articles = articles.exists()
        if articles.exists():
            p.articles_size = add_suffix(articles.stat().st_size)
        p.has_annotations = False
    return render(request, 'index.html', locals())


@login_required
def download_articles(request, project: int):
    if not ProjectRole.objects.filter(user=request.user, role__label='admin', project_id=project).exists():
        raise PermissionDenied()
    articles = articles_file(project)
    if not articles.exists():
        raise Http404()
    wrapper = FileWrapper(articles.open('rb'))
    response = HttpResponse(wrapper, content_type='application/gzip')
    response['Content-Length'] = articles.stat().st_size
    response['Content-Disposition'] = 'attachment; filename={0}'.format(articles.name)
    return response
