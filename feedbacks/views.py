from django.shortcuts import render, redirect, get_object_or_404
from feedbacks.models import Feedback
from .forms import FeedbackForm
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

import sendgrid
import os
from sendgrid.helpers.mail import *


class FeedbackView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('feedback')
    
    def form_valid(self, form):
        response = super().form_valid(form)
 #       send_mail(form.cleaned_data['subject'], form.cleaned_data['message'], form.cleaned_data['from_email'], recipient_list=['vlyuda@mail.ru', 'kaluzhynova@gmail.com'])

   #               form.cleaned_data['from_email'], recipient_list=settings.ADMINS)
   #     messages.success(self.request, "Thank you for your feedback! We will keep in touch with you very soon!")


        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('pybursalk'))
        from_email = Email(form.cleaned_data['from_email'])
        to_email = Email('kaluzhynova@gmail.com')
        subject = form.cleaned_data['subject']
        content = Content("text/plain", form.cleaned_data['message'])
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

        messages.success(self.request, "Thank you for your feedback! We will keep in touch with you very soon!")


        return response

 
