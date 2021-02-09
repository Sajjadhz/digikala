from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class SlideShow(models.Model):
    title = models.CharField(_('Title'), max_length=128)
    subtitle = models.CharField(_('Subtitle'), max_length=256)
    image = models.ImageField(_('BackGround'), upload_to='site/slideshow')
    action_text = models.CharField(_('action text'), max_length=20)
    action_url = models.CharField(_('action url'), blank=True, max_length=200)

    def __str__(self):
        return self.title
