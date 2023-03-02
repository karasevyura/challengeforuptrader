from django.db import models
from django.urls import reverse


class BaseAbstractModel(models.Model):
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    order = models.IntegerField(
        default=10,
        verbose_name='Расположение по порядку')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Menu(BaseAbstractModel):
    title = models.CharField(max_length=20, verbose_name='Название меню')
    slug = models.SlugField(max_length=255, verbose_name='URL', null=True)
    url = models.CharField(
        max_length=255,
        verbose_name='Named URL',
        blank=True)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title

    def get_full_path(self):
        if self.url:
            full_url = reverse(self.url)
        else:
            full_url = f'/{self.slug}/'

        return full_url


class MenuItem(BaseAbstractModel):
    menu = models.ForeignKey(Menu, related_name='items', verbose_name='Меню',
                             blank=True, null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='items',
                               verbose_name='Родительский пункт меню',
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Пункт меню')
    url = models.CharField(max_length=255, blank=True,
                           verbose_name='Ссылка')
    named_url = models.CharField(max_length=255,
                                 verbose_name='Именованный URL', blank=True)

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ('order', )

    def __str__(self):
        return self.name

    def get_url(self):
        if self.named_url:
            url = reverse(self.named_url)
        elif self.url:
            url = self.url
        else:
            url = '/'

        return url
