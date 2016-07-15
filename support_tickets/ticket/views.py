from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin

from ..attachment.models import Attachment

from .forms import TicketCreationForm


class TicketCreateView(LoginRequiredMixin, CreateView):
    form_class = TicketCreationForm
    template_name = 'support_tickets/ticket_create.html'

    def get_success_url(self):
        return reverse('tickets:ticket_list')

    def form_valid(self, form):
        user = self.request.user

        # Save the ticket first, because a comment needs a ticket before it
        # can be saved.
        ticket = form['ticket'].save(commit=False)
        ticket.submitter = user
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

        return redirect(self.get_success_url())
