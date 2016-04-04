from django.db import models
from django.core.urlresolvers import reverse
from parler.models import TranslatableModel, TranslatedFields
from sorl.thumbnail import ImageField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True, unique=True)
    )

    keyword = models.OneToOneField('KeyWord', related_name='category', verbose_name=_('Keyword'), null=True, blank=True)

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
    real_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    index_page = models.BooleanField(default=False, verbose_name=_('Is in the first page?'))
    sort_order = models.PositiveSmallIntegerField(verbose_name=_('Sort order'), help_text=_(
        'Indicates how the products will be showed on the first page'), blank=True, null=True)

    keyword = models.OneToOneField('KeyWord', related_name='product', verbose_name=_('Keyword'), null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def clean(self):

        if self.index_page and not self.sort_order:
            raise ValidationError(_('If the product will be in the first page it must have sort_order'))
        super(Product, self).clean()

    def get_discount_percent(self):
        for x in self.discount.all():
            if x.is_active():
                return x.discount
        return 0

    def price(self):
        return self.real_price * (1 - self.get_discount_percent() / Decimal('100'))


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
    facebook_img = ImageField(verbose_name=_('Facebook Image'), upload_to='facebook', blank=True, null=True)

    is_index = models.BooleanField(default=False, verbose_name=_('Is index?'),
                                   help_text=_('Check if the keyword belongs to the homepage'))

    twitter_img = ImageField(verbose_name=_('Twitter Image'), upload_to='twitter', blank=True, null=True)

    # DONE: Redefine the save so there is only one keyword with is_index=True
    def save(self, *args, **kwargs):
        if self.is_index:
            index_keyowrds = KeyWord.objects.filter(is_index=True)
            for key in index_keyowrds:
                key.is_index = False
                key.save()
            self.is_index = True
        super(KeyWord, self).save(args, kwargs)


class Discount(models.Model):
    class Meta:
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    products = models.ManyToManyField('Product', related_name='discount', verbose_name=_('Products'), blank=True)

    def is_active(self):
        from datetime import datetime, timedelta, timezone

        return self.valid_from <= datetime.now(tz=timezone(timedelta(hours=-5))) <= self.valid_to

    def clean(self):
        if self.valid_from >= self.valid_to:
            raise ValidationError(_('valid_from can\'t be less than valid_to. Asshole!'))
        super(Discount, self).clean()


class FrontPagePicture(TranslatableModel):
    class Meta:
        verbose_name = _('Main Page picture')
        verbose_name_plural = _('Main Page pictures')

    translation = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name=_('Title'),
                               help_text=_('This will be set as picture\'s alt')),
        button_text=models.CharField(max_length=200, verbose_name=_('Button title'))
    )
    url = models.URLField(verbose_name=_('URL'), blank=True, null=True)
    front_img = ImageField(verbose_name=_('Front Image'), upload_to='/front')


class MyUser(User):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username
