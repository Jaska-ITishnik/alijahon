import re

from django.core.exceptions import ValidationError
from django.db.models import PositiveIntegerField, ImageField, CharField, ForeignKey, CASCADE, TextChoices, TextField, \
    DateTimeField, BooleanField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import TimeSlugBased, TimeBasedModel


class Product(TimeSlugBased):
    price = PositiveIntegerField(verbose_name=_('Price'), help_text=_("In sum"))
    photo = ImageField(verbose_name=_('Photo'), upload_to='products/%Y/%m/%d')
    quantity = PositiveIntegerField(verbose_name=_('Quantity'))
    discount = CharField(verbose_name=_('Discount'), max_length=255, null=True, blank=True)
    category = ForeignKey('apps.Category', CASCADE, verbose_name=_('Category'))
    description = CKEditor5Field(verbose_name=_('Description'))
    product_fee = PositiveIntegerField(verbose_name=_('Product fee'), help_text=_("In sum"), null=True, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Order(TimeBasedModel):
    class Status(TextChoices):
        NEW = 'new', 'New'
        ARCHIVED = 'archived', 'Archived'
        READY_TO_DELIVER = 'ready_to_deliver', 'Ready to deliver'
        DELIVERING = 'delivering', 'Delivering'
        DELIVERED = 'delivered', 'Delivered'
        BROKEN = 'broken', 'Broken'
        RETURNED = 'returned', 'Returned'
        CANCELED = 'canceled', 'Canceled'
        WAITING = 'waiting', 'Waiting'

    quantity = PositiveIntegerField(verbose_name=_('Quantity'), db_default=1)
    status = CharField(verbose_name=_('Status'), max_length=50, choices=Status.choices, default=Status.NEW)
    full_name = CharField(verbose_name=_('Fullname'), max_length=50, null=True, blank=True)
    phone = CharField(verbose_name=_('Phone'), max_length=20)
    stream = ForeignKey('apps.Stream', CASCADE, null=True, blank=True, related_name='orders', verbose_name=_('Stream'))
    product = ForeignKey('apps.Product', CASCADE, related_name='orders', verbose_name=_('Product'))
    owner = ForeignKey('apps.User', CASCADE, null=True, blank=True, verbose_name=_('Owner'))
    operator = ForeignKey('apps.User', CASCADE, limit_choices_to={'type': 'operator'}, null=True, blank=True,
                          related_name='operator_orders', verbose_name=_('Operator'))
    currier = ForeignKey('apps.User', CASCADE, limit_choices_to={'type': 'currier'}, null=True, blank=True,
                         related_name='currier_orders', verbose_name=_('Currier'))
    region = ForeignKey('apps.Region', CASCADE, null=True, blank=True, verbose_name=_('Region'))
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True, verbose_name=_('District'))
    comment = TextField(verbose_name=_('Comment'), null=True, blank=True)
    address = CharField(_('Address'), max_length=255, null=True, blank=True)
    send_date = DateTimeField(verbose_name=_('Send date'), blank=True, null=True)
    is_product_fee_added = BooleanField(verbose_name=_('Is product fee added'), null=True, blank=True, default=False)

    def clean_fields(self, exclude=None):
        self.phone = re.sub(r'[^\d]', '', self.phone)
        if len(self.phone) > 9:
            self.phone = self.phone[-9:]
        if len(self.phone) != 9:
            raise ValidationError(_('Incorrect phone number'))
        return super().clean_fields(exclude)

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.stream and self.status == Order.Status.DELIVERED and not self.is_product_fee_added:
            stream_owner = self.stream.owner
            stream_owner.balance += self.product.product_fee
            self.is_product_fee_added = True
            stream_owner.save()
        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class Stream(TimeBasedModel):
    name = CharField(verbose_name=_('Name'), max_length=255)
    discount = PositiveIntegerField(verbose_name=_('Discount'), db_default=0, null=True, blank=True)
    visit_count = PositiveIntegerField(verbose_name=_('Amount of visits'), db_default=0)
    product = ForeignKey('apps.Product', CASCADE, verbose_name=_('Product'))
    owner = ForeignKey('apps.User', CASCADE, verbose_name=_('Owner'))

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name

    @property
    def changed_price(self):
        return self.product.price - self.discount
