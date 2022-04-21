from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from validate_docbr import CPF
from django.core.exceptions import ValidationError


def validate_cpf(value):
    """
    Método para validar o CPF, caso o mesmo for invalido será disparado um erro, impedindo a criação do objeto no banco de dados
    Documentação: https://pypi.org/project/validate-docbr/
    :param value:
    :return:
    """
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(
            _('%(value)s is not a valid CPF "EXAMPLE: 123.456.789-11"'),
            params={'value': value},
        )


# Criação das modelagens de banco de dados da aplicação.
# Documentação: https://docs.djangoproject.com/en/3.1/topics/db/models/
# https://docs.djangoproject.com/en/3.1/ref/validators/
class PersonalData(models.Model):
    # AutoField é um campo para a criação de PK, omde ele incrementa seu valor de 1 em um (sequencce)
    personal_id = models.AutoField(primary_key=True)
    # OneToOneField é um campo para de relacionamento de um para um
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='personal')
    # validators é um argumento passado, quando queremos validar através de algum método que não seja Nativo
    # unique quer dizer que não podemos ter 2 valores iguais, assim, não podemos ter 2 pessoas com o mesmo cpf
    # max_length é para limitarmos a quantidade de digitos
    # blank e null = False nos diz que são valores obrigatorios. Blank e null = True é OPCIONAL
    cpf = models.CharField(unique=True, max_length=11, blank=False, null=False, validators=[validate_cpf])
    birthday = models.DateField(blank=False, null=False)
    phone = models.CharField(blank=False, null=False, max_length=11)

    def __str__(self):
        """
        A classe __str__ será utilizada para exibir o nome de um objeto de forma personalizada.
        Assim, se printarmos uma variavel que consome a classe PersonalData, será exibido o nome e sobrenome
        Lembrando, que o nome e sobrenome estão presentes na classe User, desta forma, temos que acessar user.first_name
        :return:
        """
        return f"{self.user.first_name} {self.user.last_name}"


class ProfessionalData(models.Model):
    professional_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(PersonalData, on_delete=models.CASCADE, related_name="professional")
    working = models.BooleanField()
    company_name = models.CharField(max_length=300, blank=True, null=True)
    zip_code = models.CharField(max_length=8, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    complement = models.CharField(max_length=300, blank=True, null=True)
    occupation = models.CharField(max_length=300, blank=True, null=True)
    role = models.CharField(max_length=300, blank=True, null=True)


class FinancialData(models.Model):
    financial_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(PersonalData, on_delete=models.CASCADE, related_name="financial")
    total_monthly_income = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=50)
    current_account = models.CharField(max_length=300, blank=True, null=True)
    fixed_income = models.DecimalField(decimal_places=2, max_digits=50)
    variable_income = models.DecimalField(decimal_places=2, max_digits=50)
    account_number = models.BigIntegerField(blank=False, null=False)
    agency = models.IntegerField(blank=False, null=False)
    bank = models.IntegerField(blank=False, null=False)
    digit = models.IntegerField(blank=False, null=False)


class UserProfile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(PersonalData, on_delete=models.CASCADE, related_name="profile")
    chattel = models.IntegerField(blank=False, null=False)
    movables = models.IntegerField(blank=False, null=False)
    profile_type = models.CharField(blank=False, null=False, max_length=300)


