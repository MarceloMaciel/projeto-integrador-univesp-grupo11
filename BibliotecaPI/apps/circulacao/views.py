from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView

from apps.acervo.models import Exemplar
from apps.usuarios.constants import ROLE_ADMIN, ROLE_BIBLIOTECARIO
from apps.usuarios.permissions import AdminOrBibliotecarioRequiredMixin
from apps.usuarios.utils import user_has_any_role

from .forms import DevolucaoForm, EmprestimoForm, ReservaForm
from .models import Emprestimo, Multa, Reserva


class EmprestimoListView(LoginRequiredMixin, AdminOrBibliotecarioRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'circulacao/emprestimo_list.html'
    context_object_name = 'emprestimos'

    def get_queryset(self):
        Emprestimo.objects.filter(
            status=Emprestimo.Status.ATIVO,
            data_prevista_devolucao__lt=timezone.localdate(),
        ).update(status=Emprestimo.Status.ATRASADO)
        return super().get_queryset().select_related('exemplar__livro', 'usuario')


class EmprestimoCreateView(LoginRequiredMixin, AdminOrBibliotecarioRequiredMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'circulacao/form.html'
    success_url = reverse_lazy('circulacao:emprestimo_list')

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        exemplar = self.object.exemplar
        exemplar.status = Exemplar.Status.EMPRESTADO
        exemplar.save(update_fields=['status'])
        messages.success(self.request, 'Empréstimo registrado com sucesso.')
        return response


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'circulacao/reserva_list.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        queryset = Reserva.objects.select_related('livro', 'usuario')
        if user_has_any_role(self.request.user, [ROLE_ADMIN, ROLE_BIBLIOTECARIO]):
            return queryset
        return queryset.filter(usuario=self.request.user)


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'circulacao/form.html'
    success_url = reverse_lazy('circulacao:reserva_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        if not form.instance.data_expiracao:
            form.instance.data_expiracao = timezone.localdate() + timedelta(days=3)
        messages.success(self.request, 'Reserva criada com sucesso.')
        return super().form_valid(form)


@login_required
@transaction.atomic
def registrar_devolucao(request, pk):
    if not user_has_any_role(request.user, [ROLE_ADMIN, ROLE_BIBLIOTECARIO]):
        messages.error(request, 'Você não possui permissão para registrar devolução.')
        return redirect('home')

    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.status == Emprestimo.Status.DEVOLVIDO:
        messages.warning(request, 'Este empréstimo já foi devolvido.')
        return redirect('circulacao:emprestimo_list')

    if request.method == 'POST':
        form = DevolucaoForm(request.POST, emprestimo=emprestimo)
        if form.is_valid():
            data_devolucao = form.cleaned_data['data_devolucao']
            emprestimo.data_devolucao = data_devolucao
            emprestimo.status = Emprestimo.Status.DEVOLVIDO
            emprestimo.save(update_fields=['data_devolucao', 'status'])

            exemplar = emprestimo.exemplar
            exemplar.status = Exemplar.Status.DISPONIVEL
            exemplar.save(update_fields=['status'])

            dias_atraso = max((data_devolucao - emprestimo.data_prevista_devolucao).days, 0)
            if dias_atraso > 0:
                Multa.objects.get_or_create(
                    emprestimo=emprestimo,
                    defaults={
                        'valor': Decimal(dias_atraso) * Decimal('1.50'),
                        'motivo': f'Atraso de {dias_atraso} dia(s) na devolução.',
                    },
                )

            messages.success(request, 'Devolução registrada com sucesso.')
            return redirect('circulacao:emprestimo_list')
    else:
        form = DevolucaoForm(initial={'data_devolucao': timezone.localdate()}, emprestimo=emprestimo)

    return render(request, 'circulacao/devolucao_form.html', {'form': form, 'emprestimo': emprestimo})


@login_required
@transaction.atomic
@require_POST
def renovar_emprestimo(request, pk):
    if not user_has_any_role(request.user, [ROLE_ADMIN, ROLE_BIBLIOTECARIO]):
        messages.error(request, 'Você não possui permissão para renovar empréstimos.')
        return redirect('home')

    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.status == Emprestimo.Status.DEVOLVIDO:
        messages.warning(request, 'Empréstimos já devolvidos não podem ser renovados.')
        return redirect('circulacao:emprestimo_list')

    emprestimo.data_prevista_devolucao += timedelta(days=7)
    if emprestimo.data_prevista_devolucao >= timezone.localdate():
        emprestimo.status = Emprestimo.Status.ATIVO
    emprestimo.save(update_fields=['data_prevista_devolucao', 'status'])

    messages.success(request, 'Empréstimo renovado por mais 7 dias.')
    return redirect('circulacao:emprestimo_list')
