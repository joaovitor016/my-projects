from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import *
from django.core.mail import send_mail
from InfinityInvest.settings import EMAIL_HOST_USER
from password_generator import PasswordGenerator
from django.contrib.auth.hashers import make_password


def send_text(send_to):
    """

    :param send_to:
    :return:

    Método para criar uma senha de forrma aleatória e encaminhar por e-mail para o usuário,
    de acordo com o e-mail por parametro

    Documentação:
    https://pypi.org/project/random-password-generator/
    https://docs.djangoproject.com/en/3.1/topics/email/

    """
    subject_header = "Seja Bem-vindo a Infinity Invest"
    pwo = PasswordGenerator()
    pwo.minlen = 10
    pwo.maxlen = 15
    pwo.minuchars = 2
    pwo.minlchars = 3
    pwo.minnumbers = 1
    pwo.minschars = 1
    pwd = pwo.generate()
    message_text = f"Olá sejá bem-vindo!\n\nSua Senha de acesso é: {pwd} \n\n" \
        f"Recomendamos que realize a troca da sua senha.\n\nAtt"
    send_mail(subject=subject_header, message=message_text, from_email=EMAIL_HOST_USER, recipient_list=[send_to],
              fail_silently=False)
    return pwd


class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_active = serializers.BooleanField(write_only=False, required=False, default=True)
    is_superuser = serializers.BooleanField(write_only=False, required=False, default=False)
    is_staff = serializers.BooleanField(write_only=False, required=False, default=False)

    class Meta:
        model = User
        fields = ['url', 'pk', 'username', 'first_name', 'last_name', 'email', 'password',
                  'is_active', 'is_superuser', 'is_staff']
        extra_kwargs = {'password': {'required': False}}

    def create(self, validated_data):
        validated_data['password'] = make_password(send_text(validated_data.get('email')))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        if validated_data.get('password') != instance.password and validated_data.get('password') is not None:
            instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """
        Documentação:
        https://www.django-rest-framework.org/tutorial/1-serialization/
        https://docs.djangoproject.com/en/3.1/topics/db/queries/
    """
    class Meta:
        """
            model = Tabela do banco de dados
            fields = Campos que irão aparecer no json de GET/POST/PUT
            extra_kwargs = detalhe de opções de cada campo
        """
        model = UserProfile
        fields = ('url', 'pk', 'profile_id', 'user', 'chattel', 'movables', 'profile_type')
        extra_kwargs = {'chattel': {'required': False}, 'movables': {'required': False}}

    def __init__(self, *args, **kwargs):
        # Construtor do método
        super(UserProfileSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        # Criação do Objeto seguinda a documentação do Django Objects
        profile = UserProfile(**validated_data)
        profile.save()
        return profile

    def update(self, instance, validated_data):
        # Alterando todos os valores, exceto a PK e o campo de usuário
        instance.chattel = validated_data.get('chattel', instance.chattel)
        instance.movables = validated_data.get('movables', instance.movables)
        instance.profile_type = validated_data.get('profile_type', instance.profile_type)
        instance.save()
        return instance


class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = ('url', 'pk', 'financial_id', 'user', 'total_monthly_income', 'current_account', 'fixed_income',
                  'variable_income', 'account_number', 'agency', 'bank', 'digit')
        extra_kwargs = {'current_account': {'required': False},
                        'fixed_income': {'required': False, 'default': 0},
                        'variable_income': {'required': False, 'default': 0}}

    def __init__(self, *args, **kwargs):
        super(FinancialDataSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        financial = FinancialData(**validated_data)
        financial.save()
        return financial

    def update(self, instance, validated_data):
        instance.total_monthly_income = validated_data.get('total_monthly_income', instance.total_monthly_income)
        instance.current_account = validated_data.get('current_account', instance.current_account)
        instance.fixed_income = validated_data.get('fixed_income', instance.fixed_income)
        instance.variable_income = validated_data.get('variable_income', instance.variable_income)
        instance.account_number = validated_data.get('account_number', instance.account_number)
        instance.agency = validated_data.get('agency', instance.agency)
        instance.bank = validated_data.get('bank', instance.bank)
        instance.digit = validated_data.get('digit', instance.digit)
        instance.save()
        return instance


class ProfessionalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalData
        fields = ('url', 'pk', 'professional_id', 'user', 'working', 'company_name', 'zip_code', 'city', 'address',
                  'number', 'complement', 'occupation', 'role')
        extra_kwargs = {'company_name': {'required': False}, 'zip_code': {'required': False},
                        'city': {'required': False}, 'address': {'required': False},
                        'number': {'required': False, 'default': 0}, 'complement': {'required': False},
                        'occupation': {'required': False}, 'role': {'required': False}}

    def __init__(self, *args, **kwargs):
        super(ProfessionalDataSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        professional = ProfessionalData(**validated_data)
        professional.save()
        return professional

    def update(self, instance, validated_data):
        instance.working = validated_data.get('working', instance.working)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.zip_code = validated_data.get('zip_code', instance.zip_code)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.number = validated_data.get('number', instance.number)
        instance.complement = validated_data.get('complement', instance.complement)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


class PersonalDataSerializer(serializers.ModelSerializer):
    """
    Os campos abaixos setados como read_only, são retornado para que possamos puxar
    todos os dados de um usuário através de uma unica URL da API, onde ele irá criar
    uma chave com o nome da variavel e os valores que possui no fields da classe que a variavel está recebendo, por exemplo
    "user_data": {
        "pk": 3,
        "email": "email@hotmail.com",
        "first_name": "Primeiro Nome",
        "last_name": "Sobrenome",
        "password": "Senha Criptografada"
    }

    OBS: as informações são puxadas através do campo de relcionamento OneToOne, onde a classe PersonalData está interligada com as demais
    """
    user_data = UserSerializer(read_only=True, source='user')
    professional_data = ProfessionalDataSerializer(read_only=True, source='professional')
    financial_data = FinancialDataSerializer(read_only=True, source='financial')
    profile_data = UserProfileSerializer(read_only=True, source='profile')

    class Meta:
        model = PersonalData
        fields = ('url', 'pk', 'personal_id', 'user', 'cpf', 'birthday', 'phone', 'user_data',
                  'professional_data', 'financial_data', 'profile_data')
        extra_kwargs = {'birthday': {'format': "%d/%m/%Y", "input_formats": ["%d/%m/%Y", ]}}

    def __init__(self, *args, **kwargs):
        super(PersonalDataSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        personal = PersonalData(**validated_data)
        personal.save()
        return personal

    def update(self, instance, validated_data):
        instance.cpf = validated_data.get('cpf', instance.cpf)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
