import uuid
from django.db import models
from month.models import MonthField

class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expense_type = models.CharField(max_length=50, choices=[
        ('essencial', 'Essencial'),
        ('pessoal', 'Pessoal'),
        ('financeiro', 'Financeiro'),
    ])
    categ_main_name = models.CharField(max_length=255)
    categ_sub_name = models.CharField(max_length=255)
    fixed_expense = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Categoria de Despesa"
        verbose_name_plural = "Categorias de Despesa"
        unique_together = ('expense_type', 'categ_main_name', 'categ_sub_name')

    def __str__(self):
        return self.categ_sub_name


class Bank(models.Model):
    bank_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bank_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.bank_name


class Payer(models.Model):
    payer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.payer_name


class Owner(models.Model):
    owner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.owner_name


class Transaction(models.Model):
    expense_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payer = models.ForeignKey(Payer, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(Owner, on_delete=models.DO_NOTHING)
    expense_date = models.DateField()
    reference_month = MonthField("Mes da despesa")
    description = models.CharField(max_length=255)
    expense_location = models.CharField(max_length=255, choices=[('Dinheiro', 'Dinheiro'), ('Cartão', 'Cartão')])
    in_installments = models.BooleanField(default=False)
    installment_number = models.IntegerField(default=1)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.expense_location == 'Cartão':
            if self.in_installments and (self.installment_number < 2):
                raise ValidationError({'installment_number': "Número de parcelas deve ser maior que 1 se parcelado."})
            if not self.bank:
                raise ValidationError({'bank': "Banco é obrigatório para despesas em dinheiro."})
        else:
            self.in_installments = False
            self.installment_number = 1
            self.bank = None

    def __str__(self):
        return f"{self.description} - {self.amount}"
