from django.contrib.auth.models import User
from core.models import PersonalData, FinancialData, ProfessionalData, UserProfile


def get_personal(user):
    user = User.objects.get(username=user)
    personal = PersonalData.objects.get(user=user.id)
    return personal


def get_personal_by_id(personal_id):
    personal = PersonalData.objects.get(pk=personal_id)
    return personal


def get_class(find_user):
    personal = get_personal(find_user)
    try:
        # Se o objeto financial já existir. Quer dizer, que o método será de PUT
        financial = FinancialData.objects.get(user=personal.pk)
        method_type = "PUT"
    except FinancialData.DoesNotExist:
        method_type = "POST"
        financial = None

    try:
        profile = UserProfile.objects.get(user=personal.pk)
    except UserProfile.DoesNotExist:
        profile = None

    try:
        professional = ProfessionalData.objects.get(user=personal.pk)
    except ProfessionalData.DoesNotExist:
        professional = None

    try:
        user = User.objects.get(pk=personal.user_id)
    except User.DoesNotExist:
        user = None

    return method_type, personal, professional, profile, financial, user


def custom_kwargs(request, personal, professional, profile, financial, user, method_type):
    kwargs = request.data
    if kwargs:
        """
            Setando dados obrigatórios para requisição, que não são preenchidos pelo front
        """
        # PersonalData
        kwargs['user'] = user.pk

        # User
        kwargs['user_data']['is_staff'] = user.is_staff
        kwargs['user_data']['is_superuser'] = user.is_superuser
        kwargs['user_data']['is_active'] = user.is_active

        # ProfessionalData
        kwargs['professional_data']['user'] = personal.pk
        if method_type == "PUT":
            kwargs['professional_data']['professional_id'] = professional.pk

        # FinancialData
        kwargs['financial_data']['user'] = personal.pk
        if method_type == "PUT":
            kwargs['financial_data']['financial_id'] = financial.pk

        # UserProfile
        kwargs['profile_data']['user'] = personal.pk
        if method_type == "PUT":
            kwargs['profile_data']['profile_id'] = profile.pk

    return kwargs
