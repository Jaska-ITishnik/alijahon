from django.utils.translation import gettext_lazy as _

from apps.models import User, Order
from apps.models.proxy_managers import OperatorUserManager, AdminUserManager, CustomerUserManager, CurrierUserManager


class OperatorUserProxy(User):
    objects = OperatorUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Operator')
        verbose_name_plural = _('Operators')


class OperatorStatisticUserProxy(User):
    objects = OperatorUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Operator Statistics')
        verbose_name_plural = _('Operators Statistics')


class AdminUserProxy(User):
    objects = AdminUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')


class CustomerUserProxy(User):
    objects = CustomerUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class CurrierUserProxy(User):
    objects = CurrierUserManager()

    class Meta:
        proxy = True
        verbose_name = _('Currier')
        verbose_name_plural = _('Curriers')


class NewOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('New')
        verbose_name_plural = _('New')


class ArchivedOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Archived')
        verbose_name_plural = _('Archived')


class ReadyToDeliverOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Ready')
        verbose_name_plural = _('Readies')


class DeliveringOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Delivering')
        verbose_name_plural = _('Delivering')


class DeliveredOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Delivered')
        verbose_name_plural = _('Delivered')


class BrokenOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Broken')
        verbose_name_plural = _('Broken')


class ReturnedOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Returned')
        verbose_name_plural = _('Returned')


class CanceledOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Canceled')
        verbose_name_plural = _('Canceled')


class WaitingOrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = _('Waiting')
        verbose_name_plural = _('Waiting')
