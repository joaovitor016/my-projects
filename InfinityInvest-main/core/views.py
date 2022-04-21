from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render
from core.serializers import PersonalDataSerializer, UserProfileSerializer, FinancialDataSerializer, \
    ProfessionalDataSerializer, UserSerializer
from core.utility import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes


@api_view(['GET', 'POST', 'PUT'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@login_required(login_url='/login/')
def home_page(request):
    template_name = 'home.html'
    serializer_context = {
        'request': request,
    }
    render_kwargs = {'client_bar': 'active'}

    # Recuperando dados dos objetoes
    method_type, personal, professional, profile, financial, user = get_class(request.user)
    id_personal = personal.pk
    render_kwargs['id_personal'] = id_personal
    render_kwargs['method_type'] = method_type

    if request.method in ("POST", "PUT"):
        # Criando um dicionário custumizado para os métodos POST/PUT
        kwargs = custom_kwargs(request, personal, professional, profile, financial, user, method_type)
        if method_type == "PUT":
            serializer = UserSerializer(user, data=kwargs['user_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar UserProfile: {serializer.errors}")

            # PersonalData
            serializer = PersonalDataSerializer(personal, data=kwargs, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar PersonalData: {serializer.errors}")

            # ProfessionalData
            serializer = ProfessionalDataSerializer(professional, data=kwargs['professional_data'],
                                                    context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar ProfessionalData: {serializer.errors}")

            # FinancialData
            serializer = FinancialDataSerializer(financial, data=kwargs['financial_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar FinancialData: {serializer.errors}")

            # UserProfile
            serializer = UserProfileSerializer(profile, data=kwargs['profile_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar UserProfile: {serializer.errors}")
        elif method_type == "POST":
            serializer = UserSerializer(user, data=kwargs['user_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar UserProfile: {serializer.errors}")

            # PersonalData
            serializer = PersonalDataSerializer(personal, data=kwargs, context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar PersonalData: {serializer.errors}")

            # ProfessionalData
            serializer = ProfessionalDataSerializer(data=kwargs['professional_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar ProfessionalData: {serializer.errors}")

            # FinancialData
            serializer = FinancialDataSerializer(data=kwargs['financial_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar FinancialData: {serializer.errors}")

            # UserProfile
            serializer = UserProfileSerializer(data=kwargs['profile_data'], context=serializer_context)
            if serializer.is_valid():
                serializer.save()
            else:
                print(f"Erro ao atualizar UserProfile: {serializer.errors}")

    # Sempre deverá retornar o GET do usuário
    serializer = PersonalDataSerializer(personal, context=serializer_context)
    render_kwargs['serializer'] = serializer.data
    return Response(render_kwargs, status=status.HTTP_200_OK, template_name=template_name)


@login_required(login_url='/login/')
def logout_session(request):
    logout(request)
    return HttpResponseRedirect("/")


def login_session(request):
    if request.method == 'POST':
        try:
            # Gather the username and password provided by the user.
            # This information is obtained from the login form.
            try:
                username = request.POST.get('username', False)
                client = User.objects.filter(email=username)
                username = client[0].username
            except User.DoesNotExist:
                return render(request, 'login.html', {})

            password = request.POST.get('password', False)
            user = authenticate(username=username, password=password)
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
            # Bad login details were provided. So we can't log the user in.
        except:
            return render(request, 'login.html', {})
    return render(request, 'login.html', {})


@login_required(login_url='/login/')
def change_password(request):
    serializer_context = {
        'request': request,
    }
    render_kwargs = {}
    personal = get_personal(request.user)
    serializer = PersonalDataSerializer(personal, context=serializer_context)
    render_kwargs['serializer'] = serializer.data

    if request.method == "POST":
        new_password = request.POST.get('new_password', False)
        user_data = serializer.data['user_data']
        user_data['password'] = new_password
        try:
            user = User.objects.get(pk=personal.user_id)
            serializer_user = UserSerializer(user, data=user_data, context=serializer_context)
            if serializer_user.is_valid():
                serializer_user.save()
                return HttpResponseRedirect("/")
            else:
                print(f"Erro ao atualizar UserProfile: {serializer_user.errors}")
                return render(request, 'change_password.html', {'error': serializer_user.errors})
        except User.DoesNotExist:
            user = None

    return render(request, 'change_password.html', {})


@api_view(['GET', 'PUT'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
@permission_classes([IsAuthenticated, IsAdminUser])
@login_required(login_url='/login/')
def customers_list(request):
    template_name = 'customers_list.html'
    serializer_context = {
        'request': request,
    }
    render_kwargs = {'customers_bar': 'active'}

    if request.method == "PUT":
        if request.data:
            personal = get_personal_by_id(request.data['personal_id'])
            serializer = PersonalDataSerializer(personal, context=serializer_context)
            user_data = serializer.data['user_data']
            user_data['is_staff'] = request.data['is_staff']
            try:
                user = User.objects.get(pk=personal.user_id)
                serializer_user = UserSerializer(user, data=user_data, context=serializer_context)
                if serializer_user.is_valid():
                    serializer_user.save()
            except User.DoesNotExist:
                pass
    serializer = PersonalDataSerializer(PersonalData.objects.all().order_by('user__first_name', 'user__last_name'),
                                        many=True, context=serializer_context)
    render_kwargs['serializer'] = serializer.data
    return Response(render_kwargs, status=status.HTTP_200_OK, template_name=template_name)


@login_required(login_url='/login/')
def token(request):
    render_kwargs = {'token_bar': 'active'}
    return render(request, 'token.html', render_kwargs)


@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def register(request):
    template_name = 'register.html'
    serializer_context = {
        'request': request,
    }
    render_kwargs = {'customers_bar': 'active'}
    if request.method == "POST":
        kwargs = request.data
        if kwargs and 'user_data' in kwargs:
            kwargs['user_data']['username'] = kwargs['user_data']['email']
            # UserSerializer
            serializer_user = UserSerializer(data=kwargs['user_data'], context=serializer_context)
            if serializer_user.is_valid():
                serializer_user.save()
                user = User.objects.get(email=kwargs['user_data']['email'])
                kwargs['user'] = user.pk
                serializer_personal = PersonalDataSerializer(data=kwargs, context=serializer_context)
                if serializer_personal.is_valid():
                    serializer_personal.save()
                    return HttpResponseRedirect("/")
                else:
                    user.delete()
                    print(f"Erro para criar PersonalData: {serializer_personal.errors}")
            else:
                print(f"Erro para criar User: {serializer_user.errors}")

    return Response(render_kwargs, status=status.HTTP_200_OK, template_name=template_name)
