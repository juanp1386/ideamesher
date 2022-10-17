from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ObjectDoesNotExist
# from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Project(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_tree=models.TextField(blank=True)
    created_date=models.DateTimeField(default=timezone.now)
    title=models.CharField(max_length=200, blank=True)


class Entry(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('R', 'Requirement'),
        ('C', 'Concept'),
        ('D', 'Design'),
        ('V', 'Validation'),
    ]
    project=models.ForeignKey('main_app.Project', on_delete=models.CASCADE, related_name='entries')
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry_id=models.CharField(max_length=200, unique=True)
    entry_type=models.CharField(max_length=1, choices=ENTRY_TYPE_CHOICES) # R, C, D, V
    number_of_children_entries=models.IntegerField(default=0)#requirement not considered
    number_of_sub_requirements=models.IntegerField(blank=True, default=0)#empty for everything except for concept, error proof in the future
    title=models.CharField(max_length=200)
    short_desc=models.CharField(max_length=300)
    #text=RichTextUploadingField()
    text=RichTextUploadingField(config_name='default',verbose_name='Content',null=True,blank=True)
    #text=RichTextUploadingField(config_name='default')
    ###text=CKEditor5Field('Text', config_name='extends')   ##### for django-ckeditor-5 ###########################
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True, null=True)

    def publish(self):
        print(self.entry_type)
        self.published_date=timezone.now()
        self.save()
        if self.entry_type=='C':
            requirement_counter=1
            while True:
                print(self.entry_id+'\R'+str(requirement_counter))
                try:
                    child_requirement=Entry.objects.get(entry_id=self.entry_id+'\R'+str(requirement_counter))
                    print(child_requirement)
                    child_requirement.publish()
                except ObjectDoesNotExist:
                    print("didn't find")
                    break
                if requirement_counter>200:
                    break
                requirement_counter=requirement_counter+1

    def __str__(self):
        return self.title
# Create your models here.
