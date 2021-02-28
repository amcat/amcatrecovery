from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """Model for table projects.
    Projects are the main organizing unit in AmCAT. Most other objects are
    contained within a project: articles, sets, codingjobs etc.
    Projects have users in different roles. For most authorisation questions,
    AmCAT uses the role of the user in the project that an object is contained in
    """
    __label__ = 'name'

    id = models.AutoField(primary_key=True, db_column='project_id', editable=False)

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True)

    insert_date = models.DateTimeField(db_column='insertdate', auto_now_add=True)

    active = models.BooleanField(default=True)

    # Coding fields
    #codingschemas = models.ManyToManyField("rescue.CodingSchema", related_name="projects_set")
    #codebooks = models.ManyToManyField("rescue.Codebook", related_name="projects_set")
    class Meta():
        db_table = 'projects'
        app_label = 'amcat'
        ordering = ('name',)

class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column='role_id')
    label = models.CharField(max_length=50, unique=True)

    class Meta():
        db_table = 'roles'
        app_label = 'amcat'


class ProjectRole(models.Model):
    project = models.ForeignKey("amcat.Project", db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return "%s, %s" % (self.project, self.role)

    class Meta():
        db_table = 'projects_users_roles'
        unique_together = ("project", "user")
        app_label = 'amcat'
