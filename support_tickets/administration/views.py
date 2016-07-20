# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    View
)
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin

from ..attachment.models import Attachment
from ..comment.forms import CommentCreationForm
from ..comment.models import Comment
from ..ticket.models import Ticket
from ..base.choices import TICKET_STATUS

from .forms import TicketPropertiesForm, TicketCreationForm


class AdminHomeView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    context_object_name = 'ticket_list'
    model = Ticket
    paginate_by = 10

    template_name = 'support_tickets/admin/home.html'

    def get_queryset(self, **kwargs):

        status = self.request.GET.get('status', None)

        ticket = self.model.objects.all()

        if status is not None:
            if status == 'open':
                ticket = ticket.filter(
                    Q(status=TICKET_STATUS.open) |
                    Q(status=TICKET_STATUS.reopened)
                )

            if status == 'closed':
                ticket = ticket.exclude(status=TICKET_STATUS.open)
                ticket = ticket.exclude(status=TICKET_STATUS.reopened)

        ticket = ticket.prefetch_related("category")
        ticket = ticket.prefetch_related("agent")
        ticket = ticket.order_by('status', 'priority')

        return ticket


class AdminTicketCreateView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    form_class = TicketCreationForm
    template_name = 'support_tickets/admin/ticket/create.html'
    success_message = _('The ticket was successfully created')

    def get_success_url(self):
        return reverse('tickets:admin_home')

    def form_valid(self, form):
        user = self.request.user

        # Save the ticket first, because a comment needs a ticket before it
        # can be saved.
        ticket = form['ticket'].save(commit=False)
        # Make sure the ticket has an agent
        if not ticket.agent:
            ticket.agent = user
        ticket.save()

        # Save comment
        comment = form['comment'].save(commit=False)
        comment.user = user
        comment.ticket = ticket
        comment.save()

        # Save attachments
        for each in form['attachments'].cleaned_data['attachments']:
            Attachment.objects.create(
                file=each,
                comment=comment,
                uploader=user
            )

        # Send success message
        messages.success(self.request, self.success_message)

        return redirect(self.get_success_url())


class AdminTicketDetailView(SuccessMessageMixin, FormMixin, LoginRequiredMixin, SuperuserRequiredMixin, DetailView):
    form_class = CommentCreationForm
    model = Ticket
    success_message = _('Your message was successfully sent')
    template_name = 'support_tickets/admin/ticket/view.html'

    def get_success_url(self):
        return reverse(
            'tickets:admin_ticket_detail',
            kwargs={'pk': self.object.pk}
        )

    def get_initial(self):
        return {
            'ticket': {
                'status': self.object.status
            },
        }

    def get_context_data(self, **kwargs):
        context = super(AdminTicketDetailView, self).get_context_data(**kwargs)

        # Comments
        comments = Comment.objects.filter(ticket=self.object)
        comments = comments.order_by('created')
        comments = comments.prefetch_related("user")
        comments = comments.prefetch_related("attachments")

        context['comments_list'] = comments

        # Comment form
        form = self.get_form()
        context['form'] = form

        # Ticket property form
        ticket_properties_form = TicketPropertiesForm(initial={
            'status': self.object.status,
            'category': self.object.category,
            'priority': self.object.priority,
            'agent': self.object.agent,
        })
        context['ticket_properties_form'] = ticket_properties_form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()

        if form.is_valid():
            # Update status
            new_status = form['ticket'].cleaned_data['status']
            self.object.status = new_status
            self.object.save()

            # Save comment
            comment = form['comment'].save(commit=False)
            comment.user = request.user
            comment.ticket = self.object
            comment.save()

            # Save attachments
            for each in form['attachments'].cleaned_data['attachments']:
                Attachment.objects.create(
                    file=each,
                    comment=comment,
                    uploader=request.user
                )

            return self.form_valid(form)

        else:
            return self.form_invalid(form)


class AdminTicketDeleteView(SuccessMessageMixin, LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    model = Ticket
    success_message = _('The ticket was successfully deleted')
    template_name = 'support_tickets/admin/ticket/delete.html'

    def get_success_url(self):
        return reverse('tickets:admin_home')


class AdminTicketCloseView(LoginRequiredMixin, SuperuserRequiredMixin, SingleObjectMixin, View):
    model = Ticket
    success_message = _('The ticket was successfully closed')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status != TICKET_STATUS.closed:
            self.object.status = TICKET_STATUS.closed
            self.object.save()

            # Send success message
            messages.success(self.request, self.success_message)

        return redirect('tickets:admin_ticket_detail', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        return super(AdminTicketCloseView, self).get(request, *args, **kwargs)


class AdminTicketOpenView(LoginRequiredMixin, SuperuserRequiredMixin, SingleObjectMixin, View):
    model = Ticket
    success_message = _('The ticket was successfully opened')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status != TICKET_STATUS.open and self.object.status != TICKET_STATUS.reopened:
            self.object.status = TICKET_STATUS.reopened
            self.object.save()

            # Send success message
            messages.success(self.request, self.success_message)

        return redirect('tickets:admin_ticket_detail', pk=self.object.pk)

    def post(self, request, *args, **kwargs):
        return super(AdminTicketCloseView, self).get(request, *args, **kwargs)