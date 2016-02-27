from django.db import models
from django.core.urlresolvers import reverse
from parler.models import TranslatableModel, TranslatedFields
from sorl.thumbnail import ImageField
from django.utils.translation import gettext_lazy as _


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True, unique=True)
    )

    keyword = models.OneToOneField('KeyWord', related_name='category', verbose_name=_('Keyword'))

    class Meta:
        # ordering = ('name',)
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=models.TextField(blank=True)
    )
    category = models.ForeignKey(Category, related_name='products')
    image = ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    keyword = models.OneToOneField('KeyWord', related_name='product', verbose_name=_('Keyword'))

    class Meta:
        ordering = ('-created',)
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class KeyWord(TranslatableModel):
    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')

    translations = TranslatedFields(
        keywords=models.CharField(max_length=200, verbose_name=_('Keywords'), help_text='keywords split by ;',
                                  blank=True, null=True),
        description=models.CharField(max_length=400, verbose_name=_('Google\'s description'),
                                     help_text=_('What goes inside the description metadata'), blank=True, null=True),
        facebook_msg=models.CharField(max_length=300, verbose_name=_('Facebook message'),
                                      help_text=_('What goes inside og:title metadata'), blank=True, null=True),
        twitter_msg=models.CharField(max_length=300, verbose_name=_('Twitter message'),
                                     help_text=_('What goes inside twitter:title metadata'), blank=True, null=True),
    )
    facebook_img = ImageField(verbose_name=_('Facebook Image'), upload_to='/facebook', blank=True, null=True)

    is_index = models.BooleanField(default=False, verbose_name=_('Is index?'),
                                   help_text=_('Check if the keyword belongs to the homepage'))

    twitter_img = ImageField(verbose_name=_('Twitter Image'), upload_to='/twitter', blank=True, null=True)

    # DONE: Redefine the save so there is only one keyword with is_index=True
    def save(self, *args, **kwargs):
        if self.is_index:
            index_keyowrds = KeyWord.objects.filter(is_index=True)
            for key in index_keyowrds:
                key.is_index = False
                key.save()
            self.is_index = True
        super(KeyWord, self).save(args, kwargs)
