from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import redirect, render

from apps.acervo.models import Exemplar
from apps.catalogo.models import Livro as LivroCatalogo
from apps.circulacao.models import Emprestimo
from apps.usuarios.constants import ROLE_ADMIN, ROLE_BIBLIOTECARIO
from apps.usuarios.utils import user_has_any_role

from .forms import LivroForm
from .models import PerfilUsuario


def _clear_lote_session(request):
    request.session.pop('lote_ativo_id', None)
    request.session.pop('livros_restantes', None)


def _can_manage_library(user):
    return user_has_any_role(user, [ROLE_ADMIN, ROLE_BIBLIOTECARIO])


def _apply_bootstrap(form):
    for field in form.fields.values():
        field.widget.attrs.setdefault('class', 'form-control')


@login_required
def home(request):
    try:
        perfil = request.user.perfilusuario
        if perfil.precisa_trocar_senha:
            return redirect('trocar_senha')
    except PerfilUsuario.DoesNotExist:
        pass

    context = {
        'total_livros_catalogo': LivroCatalogo.objects.count(),
        'total_exemplares_disponiveis': Exemplar.objects.filter(status=Exemplar.Status.DISPONIVEL).count(),
        'total_emprestimos_ativos': Emprestimo.objects.filter(status=Emprestimo.Status.ATIVO).count(),
    }
    return render(request, 'core/home.html', context)


@login_required
def trocar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        _apply_bootstrap(form)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            try:
                perfil = user.perfilusuario
                perfil.precisa_trocar_senha = False
                perfil.save(update_fields=['precisa_trocar_senha'])
            except PerfilUsuario.DoesNotExist:
                pass

            messages.success(request, 'Senha atualizada com sucesso.')
            return redirect('home')

        messages.error(request, 'Corrija os erros para continuar.')
    else:
        form = PasswordChangeForm(request.user)
        _apply_bootstrap(form)

    return render(request, 'core/trocar_senha.html', {'form': form})
