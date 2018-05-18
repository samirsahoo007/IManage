from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
　
　
class Roles(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=30)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Roles"
　
    def get_absolute_url(self):
        return reverse('e2admin:roles_list')
　
    def __unicode__(self):
        return self.code
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Roles, self).save(*args, **kwargs)
　
　
class Region(models.Model):
    region = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Region"
　
    def get_absolute_url(self):
        return reverse('e2admin:region_list')
　
    def __unicode__(self):
        return self.region
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Region, self).save(*args, **kwargs)
　
　
class Server(models.Model):
    ACCESSES = (
           ("Direct", "no bastion host required"),
           ("TKO Bastion", "tkdp2mgtnbh01"),
           ("NJ Bastion", "njdp2mgtnbh01"),
           ("Other", "N/A"),
        )
　
    id = models.IntegerField(editable=False, primary_key=True)
    name = models.CharField(max_length=40)
    fqdn = models.CharField(max_length=60)
    os = models.CharField(max_length=150)
    access = models.CharField(max_length=15, choices=ACCESSES)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Server"
　
    def get_absolute_url(self):
        return reverse('e2admin:server_list')
　
    def __unicode__(self):
        return self.name
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Server, self).save(*args, **kwargs)
class Product(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, unique=True)
    installdir = models.CharField(max_length=200)
    logdir = models.CharField(max_length=200)
    osuser = models.CharField(max_length=10)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Product"
　
    def get_absolute_url(self):
        return reverse('e2admin:product_list')
　
    def __unicode__(self):
        return self.name
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Product, self).save(*args, **kwargs)
　
　
class Instance(models.Model):
    ACTIVE_TYPES = (
           ("ACT", "Active - Fully Usable in E2"),
           ("INF", "Information Only - Only data is available on this instance"),
           ("DIS", "Disactivated - The instance is disactivated in E2"),
        )
    name = models.CharField(max_length=50)
    cluster = models.CharField(max_length=50, blank=True)
    profile = models.CharField(max_length=40, blank=True)
    region = models.ForeignKey(Region)
    product = models.ForeignKey(Product)
    server = models.ForeignKey(Server)
    e2active = models.CharField(max_length=3, blank=True, choices=ACTIVE_TYPES)
    associated = models.ForeignKey('self', null=True, blank=True)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
    class Meta:
        db_table = "Instance"
　
    def get_absolute_url(self):
        return reverse('e2admin:instance_list')
　
    def __unicode__(self):
        return self.name
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Instance, self).save(*args, **kwargs)
　
　
class Datacenter(models.Model):
    datacenter = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Datacenter"
　
    def get_absolute_url(self):
        return reverse('e2admin:datacenter_list')
　
    def __unicode__(self):
        return self.datacenter
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Datacenter, self).save(*args, **kwargs)
class Application(models.Model):
    appcode = models.CharField(max_length=40, unique=True)
    alternatename = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)  # 254 length RFC3696/5321-compliant email addresses
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
    newflag = models.CharField(max_length=1, editable=False)
    class Meta:
        db_table = "Application"
        permissions = (
            ("engineer", "engineering role, app man, rfw, etc"),
            ("appcontact", "rfw, non-prod app man, ability to add developers"),
            ("appdev", "rfw, non-prod app man"),
        )
　
    def get_absolute_url(self):
        return reverse('e2admin:application_list')
　
    def __unicode__(self):
        return self.appcode
　
    def save(self, *args, **kwargs):
        if not self.newflag:
            self.created = timezone.now()
            self.modified = timezone.now()
            self.newflag = 1
        else:
            self.modified = timezone.now()
　
        return super(Application, self).save(*args, **kwargs)
　
　
class ApplicationRoles(models.Model):
    application = models.ForeignKey(Application, related_name="app_role_relation")
    user = models.ForeignKey(User)
    role = models.ForeignKey(Roles)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
    class Meta:
        db_table = "ApplicationRoles"
　
    def get_absolute_url(self):
        return reverse('e2admin:application_roles_list')
　
    def __unicode__(self):
        return self.id
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(ApplicationRoles, self).save(*args, **kwargs)
　
　
class AuditRecord(models.Model):
    action = models.CharField(max_length=100)
    server = models.ForeignKey(Server, null=True, blank=True)
    instance = models.ForeignKey(Instance, null=True, blank=True)
    application = models.ForeignKey(Application, null=True, blank=True)
    user = models.CharField(max_length=20, null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True)
    result = models.CharField(max_length=30, null=True, blank=True)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "AuditRecord"
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
　
        return super(AuditRecord, self).save(*args, **kwargs)
class Environment(models.Model):
    TYPES = (
           ("UNS", "Unspecified"),
           ("DEV", "Development"),
           ("IST", "IST"),
           ("UAT", "User Acceptance Environment"),
           ("QA", "Quality Assurance Environment"),
           ("OAT", "Operational Acceptance Environment"),
           ("STG", "Staging"),
           ("PRD", "Production"),
           ("DR", "Disaster Recovery"),
        )
　
    application = models.ForeignKey(Application)
    type = models.CharField(max_length=10, choices=TYPES)  # DEV, UAT, PROD, DR, etc.
    name = models.CharField(max_length=40, unique=True)
    delivered = models.DateField()
    datacenter = models.ForeignKey(Datacenter)
    instances = models.ManyToManyField(Instance)
    gsdqueue = models.CharField(max_length=250)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
    newflag = models.CharField(max_length=1, editable=False)
　
    class Meta:
        db_table = "Environment"
　
    def get_absolute_url(self):
        return reverse('e2admin:environment_list')
　
    def __unicode__(self):
        return self.name
　
    def save(self, *args, **kwargs):
        if not self.newflag:
            self.created = timezone.now()
            self.modified = timezone.now()
            self.newflag = 1
        else:
            self.modified = timezone.now()
　
        return super(Environment, self).save(*args, **kwargs)
　
class URL(models.Model):
    url = models.CharField(max_length=254)
    description = models.CharField(max_length=200)  # Description of URL's function. e.g.: WAS Console Admin, Portal Console, etc.
    environment = models.ForeignKey(Environment)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "URL"
　
    def get_absolute_url(self):
        return reverse('e2admin:url_list')
　
    def __unicode__(self):
        return self.url
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(URL, self).save(*args, **kwargs)
　
　
class Comments(models.Model):
    comment_text = models.TextField()
    environment = models.ForeignKey(Environment, related_name="env_comment_relation", null=True, blank=True)
    application = models.ForeignKey(Application, related_name="app_comment_relation", null=True, blank=True)
    comment_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Comments"
　
    def get_absolute_url(self):
        return reverse('e2admin:comments_list')
　
    def __unicode__(self):
        return self.pk
　
    def save(self, *args, **kwargs):
        self.created = timezone.now()
　
        return super(Comments, self).save(*args, **kwargs)
class Channel_Definitions_D(models.Model):
    Channel_Name = models.CharField(max_length=254, primary_key=True)
    MQ_Manager_Name = models.CharField(max_length=200)  # Description of URL's function. e.g.: WAS Console Admin, Portal Console, etc.
    DBWRITETIME = models.DateTimeField(editable=False)
　
    class Meta:
        managed = False
        db_table = "'ITM'.'Channel_Definitions_D'"
　
    def save(self, **kwargs):
        raise NotImplementedError()
　
    def __unicode__(self):
        return self.url
　
　
class Orchestrations(models.Model):
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=200)  # Description of URL's function. e.g.: WAS Console Admin, Portal Console, etc.
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "Orchestrations"
　
    def get_absolute_url(self):
        return reverse('e2admin:orchestration_list')
　
    def __unicode__(self):
        return self.pk
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(Orchestrations, self).save(*args, **kwargs)
　
class OrchestrationOwners(models.Model):
    orchestration = models.ForeignKey(Orchestrations)
    user = models.ForeignKey(User)
    role = models.CharField(max_length=10)  # Description of URL's function. e.g.: WAS Console Admin, Portal Console, etc.
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "OrchestrationOwners"
　
    def get_absolute_url(self):
        return reverse('e2admin:OrchestrationOwners_list')
　
    def __unicode__(self):
        return self.pk
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(OrchestrationOwners, self).save(*args, **kwargs)
　
　
class OrchestrationTask(models.Model):
    task = models.CharField(max_length=20, editable=False)
    description = models.CharField(max_length=200)  # Description of URL's function. e.g.: WAS Console Admin, Portal Console, etc.
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "OrchestrationTask"
　
    def get_absolute_url(self):
        return reverse('e2admin:OrchestrationTask_list')
　
    def __unicode__(self):
        return self.pk
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
        return super(OrchestrationTask, self).save(*args, **kwargs)
　
　
class OrchestrationItems(models.Model):
    orchestration = models.ForeignKey(Orchestrations)
    ordinal = models.IntegerField(editable=True)
    instance = models.ForeignKey(Instance, blank = True, null = True)
    task = models.ForeignKey(OrchestrationTask)
    created_by = models.CharField(max_length=20, editable=False)
    created = models.DateTimeField(editable=False)
    modified_by = models.CharField(max_length=20, editable=False)
    modified = models.DateTimeField(editable=False)
　
    class Meta:
        db_table = "OrchestrationItems"
　
    def get_absolute_url(self):
        return reverse('e2admin:OrchestrationItems_list')
　
    def __unicode__(self):
        return self.pk
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
　
        return super(OrchestrationItems, self).save(*args, **kwargs)
　
　
class Regional_Admin(models.Model):
    region = models.ForeignKey(Region)
    user = models.ForeignKey(User)
　
    class Meta:
        db_table = "Regional_Admin"
　
    def get_absolute_url(self):
        return reverse('e2admin:regional_admin_list')
　
    def __unicode__(self):
        return self.region
　
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
        return super(Regional_Admin, self).save(*args, **kwargs)
　
