from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.contrib import messages

from django.conf import settings
from .models import Job, Profile, Application
from .forms import UserRegisterForm, JobForm, ApplicationForm
from django.conf import settings
from django.core.mail import send_mail, get_connection
import ssl
import certifi


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden,HttpResponse
from django.contrib import messages
from .models import Job, Profile
from .forms import ApplicationForm
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
import ssl
import certifi

def home_view(request):
    query = request.GET.get('q')
    jobs = Job.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(category__icontains=query)
        )
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

    return render(request, 'core/home.html', {'jobs': jobs, 'profile': profile})


def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'core/job_detail.html', {'job': job})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, user_type=form.cleaned_data['user_type'])
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def post_job_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if profile.user_type != 'employer':
        return HttpResponseForbidden("Only employers can post jobs.")

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('home')
    else:
        form = JobForm()

    return render(request, 'core/post_job.html', {'form': form})


# @login_required
# def apply_job_view(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#     profile = Profile.objects.get(user=request.user)

#     if profile.user_type != 'jobseeker':
#         return HttpResponseForbidden("Only job seekers can apply.")

#     if request.method == 'POST':
#         form = ApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.applicant = request.user
#             application.save()

#             send_mail(
#                 subject='New Job Application',
#                 message=f'{request.user.username} applied for {job.title}.',
#                 from_email='noreply@example.com',
#                 recipient_list=[job.posted_by.email],
#                 fail_silently=True,
#             )

#             messages.success(request, "You have successfully applied for the job.")
#             return redirect('home')
#     else:
#         form = ApplicationForm()

#     return render(request, 'core/apply_job.html', {'form': form, 'job': job})

@login_required
def employer_applications_view(request):
    profile = Profile.objects.get(user=request.user)
    if profile.user_type != 'employer':
       return HttpResponseForbidden("Only employers can view applications.")

    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__in=jobs).order_by('-applied_at')

    return render(request, 'core/employer_applications.html', {'applications': applications})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Job, Profile
from .forms import ApplicationForm
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
import ssl
import certifi

# @login_required
# def apply_job_view(request, job_id):
#     job = get_object_or_404(Job, id=job_id)
#     profile = Profile.objects.get(user=request.user)

#     if profile.user_type != 'jobseeker':
#         return HttpResponseForbidden("Only job seekers can apply.")

#     if request.method == 'POST':
#         form = ApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             application = form.save(commit=False)
#             application.job = job
#             application.applicant = request.user
#             application.save()

#             # Create secure SSL context
#             ssl_context = ssl.create_default_context(cafile=certifi.where())

#             # Set up email connection with custom SSL context
#             connection = get_connection(
#                 host=settings.EMAIL_HOST,
#                 port=settings.EMAIL_PORT,
#                 username=settings.EMAIL_HOST_USER,
#                 password=settings.EMAIL_HOST_PASSWORD,
#                 use_tls=True,
#                 ssl_context=ssl_context,
#             )

#             # Prepare and send email
#             email = EmailMessage(
#                 subject='New Job Application',
#                 body=f'{request.user.username} applied for the job: {job.title}.',
#                 from_email=settings.EMAIL_HOST_USER,
#                 to=[job.posted_by.email],
#                 connection=connection
#             )
#             email.send(fail_silently=False)

#             messages.success(request, "You have successfully applied for the job.")
#             return redirect('home')
#     else:
#         form = ApplicationForm()

#     return render(request, 'core/apply_job.html', {'form': form, 'job': job})

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@login_required
def apply_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = Profile.objects.get(user=request.user)

    if profile.user_type != 'jobseeker':
        return HttpResponseForbidden("Only job seekers can apply.")
    
    existing_application = Application.objects.filter(job=job, applicant=request.user).exists()
    if existing_application:
        messages.error(request, "You have already applied for this job.")
        return redirect('home')
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()

            ssl_context = ssl._create_unverified_context()  # Use verified one in production

            connection = get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=True,
                ssl_context=ssl_context,
            )

            try:
                # Email to employer (HTML + plain)
                subject_emp = 'New Job Application Received'
                from_email = settings.EMAIL_HOST_USER
                to_emp = [job.posted_by.email]

                text_content_emp = f"{request.user.username} has applied for the job: {job.title}."
                html_content_emp = render_to_string('core/emails/employer_notification.html', {
                    'username': request.user.username,
                    'job_title': job.title,
                })

                email_emp = EmailMultiAlternatives(subject_emp, text_content_emp, from_email, to_emp, connection=connection)
                email_emp.attach_alternative(html_content_emp, "text/html")
                email_emp.send()

                # Email to applicant (confirmation)
                subject_user = 'Job Application Confirmation'
                to_user = [request.user.email]

                text_content_user = f"Hello {request.user.username}, you applied for the job: {job.title}."
                html_content_user = render_to_string('core/emails/user_confirmation.html', {
                    'username': request.user.username,
                    'job_title': job.title,
                })

                email_user = EmailMultiAlternatives(subject_user, text_content_user, from_email, to_user, connection=connection)
                email_user.attach_alternative(html_content_user, "text/html")
                email_user.send()

                messages.success(request, "Application successful. Confirmation emails sent.")
            except Exception as e:
                
                messages.success(request, "You have successfully applied for the job.")
                return redirect('home')
    else:
        form = ApplicationForm()

    return render(request, 'core/apply_job.html', {'form': form, 'job': job})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Application

@login_required
def my_applied_jobs_view(request):
    # Get all applications for the logged-in user (job seeker)
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')

    return render(request, 'core/my_applied_jobs.html', {'applications': applications})