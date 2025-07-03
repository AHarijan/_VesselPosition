from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *


from django.http import HttpResponse
def set_cookies(request):
    cokis = HttpResponse("Cookies is Set")
    cokis.set_cookie('my_cookie', 'cookie_value', max_age=3600, secure=True)
    return cokis

def signup_pg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        country = request.POST.get('country')
        port = request.POST.get('port')
        usertype = request.POST.get('usertype')

        if CustomUser.objects.filter(CombinedField=f"{email}_{country}_{port}").exists():
            context = {
                'error': 'User already registered with this Country and Port',
            }
            return render(request, 'AuthApp/signup.html', context)
        
        # Create user with hashed password
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,  # This will be automatically hashed
            first_name=first_name.title(),
            last_name=last_name.title(),
            country=country.upper(),
            port=port.upper(),
            usertype=usertype,
            CombinedField=f"{email}_{country}_{port}",
        )
        
        return render(request, 'AuthApp/signin.html', {'error': 'Registeration Succesful!'})  # Redirect to login page with success message
    return render(request, 'AuthApp/signup.html')

####### USER SIGNUP REQUEST VIA EMAIL #########
from django.core.mail import send_mail

def usersignup_pg(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        port = request.POST.get('port')

        subject = "New User Registration Request"
        message = f"""
        A new User have requested for registration:
        First Name = {first_name}
        Last Name = {last_name}
        Email ID = {email}
        Counrty = {country}
        Port = {port}
        """

        sender_email = "donot.reply.automail1234@gmail.com"
        recipient_email = "alakar_harijan@outlook.com"
        send_mail(subject, message, sender_email, [recipient_email])

        return redirect('usersignupconf')
    return render(request, 'AuthApp/UserSignup.html')

####### USER SIGNUP CONFIRMATION PAGE #########
def usersignupConf_pg(request):
    return render(request, 'AuthApp/UserSignupConfirmation.html')

####### USER LOGGIN IN WITH SESSION #########
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import login as auth_login

def index_pg(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['password'] = user.password
            request.session['country'] = user.country
            request.session['port'] = user.port
            request.session['usertype'] = user.usertype
            request.session.modified = True
            request.session.set_expiry(3600)

            return redirect('lineupform')
        else:
            return render(request, 'AuthApp/signin.html', {'error': 'Invalid Credentials'})
        
    return render(request, 'AuthApp/signin.html')

####### PASSWORD RESET LINK SENT TO USERS MAIL ID #########
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings

def forgotpass_pg(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('resetpass', kwargs={'reset_id': new_password_reset.reset_id})
            email_body = f'Reset your password using the link below:\n\n\n http://127.0.0.1:8000{password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )
          
            email_message.fail_silently = False
            email_message.send()

            # return redirect('resetpasssent')
            return redirect('resetpasssent', reset_id=new_password_reset.reset_id)

        except CustomUser.DoesNotExist:
            return redirect('forgotpass', {'error': "No user with email '{email}' found"})
    return render (request,'AuthApp/forgotpass.html')

####### PASSWORD RESET #########
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password

def resetpass_pg(request, reset_id):

    try:
        reset_instance  = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # passwords_have_error = False

            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return render(request, 'AuthApp/resetpass.html', {'reset_id': reset_id})

            expiration_time = reset_instance.created_when + timezone.timedelta(minutes=10)
            if timezone.now() > expiration_time:
                reset_instance.delete()
                messages.error(request, 'Reset link has expired')
                return redirect('forgotpass')

            user = reset_instance.user
            user.Password=make_password(password)
            user.save()
                
                # delete reset id after use
            reset_instance.delete()

                # redirect to login
            messages.success(request, 'Password reset. Proceed to login')
            return redirect('signin')

            # else:
            #     # redirect back to password reset page and display errors
            #     return redirect('resetpass', reset_id=reset_id)
    
    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgotpass')

    return render (request,'AuthApp/resetpass.html', {'reset_id': reset_id})

def resetpasssent_pg(request, reset_id):

        if PasswordReset.objects.filter(reset_id=reset_id).exists():
            return render(request, 'AuthApp/passreset_sent.html')
        else:
            # redirect to forgot password page if code does not exist
            messages.error(request, 'Invalid reset id')
            return redirect('forgotpass')

####### ENTERING LINEUP DATA #########        
from django.contrib.auth.decorators import login_required
@login_required
def LineupForm_pg(request):
    # Get current user's information from session
    user_type = request.session.get('UserType')
    user_port = request.session.get('Port', '').strip()
    
    # Handle form submission
    if request.method == "POST":
        # Extract all form data
        lineup_date = request.POST['lineupdate']
        port = request.POST['port']
        berth = request.POST['berth']
        imo_no = request.POST['imono']
        slt = request.POST['vesselSlt']
        vessel = request.POST['vessel']
        loa = request.POST['loa']
        beam = request.POST['beam']
        draft = request.POST['draft']
        eta_ata_date = request.POST['etadate'] if request.POST['etadate'] else None
        eta_ata_time = request.POST['etatime'] if request.POST['etatime'] else None
        etb_atb_date = request.POST['etbdate'] if request.POST['etbdate'] else None
        etb_atb_time = request.POST['etbtime'] if request.POST['etbtime'] else None
        etd_atd_date = request.POST['etcdate'] if request.POST['etcdate'] else None
        etd_atd_time = request.POST['etctime'] if request.POST['etctime'] else None
        cargo1 = request.POST['cargo1']
        cargoqty1 = request.POST['cargoqty1']
        cargounits1 = request.POST['cargoqtyU1']
        cargo2 = request.POST['cargo2']
        cargoqty2 = request.POST.get('cargoqty2', 0)
        cargounits2 = request.POST['cargoqtyU2']
        cargo3 = request.POST['cargo3']
        cargoqty3 = request.POST.get('cargoqty3', 0)
        cargounits3 = request.POST['cargoqtyU3']
        vesseltype = request.POST['vesseltype']
        operations = request.POST['operation']
        shipper = request.POST['shipper']
        receiver = request.POST['receiver']
        principal = request.POST['principal']
        owner = request.POST['owner']
        c_f = request.POST['C/F']
        lastport = request.POST['lastport']
        nextport = request.POST['nextport']
        loadport = request.POST['loadPort']
        dischargeport = request.POST['dischargePort']
        chartereragent = request.POST['cAgent']
        ownersagent = request.POST['agent']
        currentstatus = request.POST['status']
        remarks = request.POST.get('textarea')

        # Create and save new LineUpForm entry
        obj = LineUpForm(
            LineUp_Date=lineup_date, Port=port.upper(), Berth=berth, IMO_No=imo_no, 
            Slt=slt, Vessel=vessel.upper(), LOA=loa, Beam=beam, Draft=draft,
            ETA_ATA_Date=eta_ata_date, ETA_ATA_Time=eta_ata_time,
            ETB_ATB_Date=etb_atb_date, ETB_ATB_Time=etb_atb_time,
            ETD_ATD_Date=etd_atd_date, ETD_ATD_Time=etd_atd_time,
            Cargo1=cargo1.upper(), CargoQty1=cargoqty1, CargoUnits1=cargounits1,
            Cargo2=cargo2.upper(), CargoQty2=cargoqty2, CargoUnits2=cargounits2,
            Cargo3=cargo3.upper(), CargoQty3=cargoqty3, CargoUnits3=cargounits3,
            VesselType=vesseltype, Operations=operations,
            Shipper=shipper.upper(), Receiver=receiver.upper(), Principal=principal.upper(),
            Owner=owner.upper(), C_F=c_f, LastPort=lastport.upper(), NextPort=nextport.upper(),
            LoadPort=loadport.upper(), DischargePort=dischargeport.upper(),
            ChartererAgent=chartereragent.upper(), OwnersAgent=ownersagent.upper(),
            CurrentStatus=currentstatus.upper(), Remarks=remarks.upper()
        )
        obj.save()

        return redirect('lineupform')



    ports_queryset = Port_Berth_Form.objects.all()
    lineup_queryset = LineUpForm.objects.all()
    user_berths = []
    user_ports = []

    # Retrieve selected port from request
    selected_port = request.GET.get('port')

    # Apply port filtering for regular users
    if user_type == 'user' and user_port:
        user_ports = [p.strip() for p in user_port.split(',') if p.strip()]
        ports_queryset = ports_queryset.filter(Port__in=user_ports)

        # If a port is selected, filter lineup by that specific port, otherwise, filter by all assigned ports
        if selected_port and selected_port in user_ports:
            lineup_queryset = LineUpForm.objects.filter(Port__iexact=selected_port)
        else:
            lineup_queryset = LineUpForm.objects.filter(Port__in=user_ports)

        user_berths = Port_Berth_Form.objects.filter(
            Port__in=user_ports
        ).values_list('Berth', flat=True).order_by('Berth').distinct()

    # Prepare data for template
    ports = ports_queryset.values_list('Port', flat=True).distinct().order_by('Port')
    datas = lineup_queryset.order_by('CurrentStatus')

    # Set default_port to selected_port if available
    default_port = selected_port if selected_port else (user_ports[0] if user_ports else '')

    return render(request, 'Pages/lineupForm.html', {
        'datas': datas,
        'ports': ports,
        'user_berths': list(user_berths),
        'default_port': default_port,
        'is_user': user_type == 'user',
        'user_ports': user_ports,
    })


@login_required
def AddPortBerth_pg(request):
    if request.method == 'POST':
        # Extract Section 1 data (Country and Port)
        country = request.POST.get('country')
        port = request.POST.get('port')
        pic1_mail = request.POST.get('1st_pic')
        pic2_mail = request.POST.get('2st_pic')
        pic3_mail = request.POST.get('3st_pic')

        # Extract Section 2 data (multiple entries)
        berths = request.POST.getlist('berth')
        PermissibleDraft = request.POST.getlist('PermissibleDraft')
        LOBerth = request.POST.getlist('LOBerth')
        cargos_handled = request.POST.getlist('cargoType')
        terminals = request.POST.getlist('terminal')
        BerthRemarks = request.POST.getlist('BerthRemarks')

        # Validate that all fields are present
        if country and port and berths and cargos_handled and terminals:
            # Save each Berth entry
            for i in range(len(berths)):
                Port_Berth_Form.objects.create(
                    Country=country.upper(),
                    Port=port.upper(),
                    PIC1Mail=pic1_mail.lower(),
                    PIC2Mail=pic2_mail.lower(),
                    PIC3Mail=pic3_mail.lower(),
                    Berth=berths[i],
                    PermissibleDraft=PermissibleDraft[i],
                    LOBerth=LOBerth[i],
                    Cargos_Handled_on_Berth=cargos_handled[i],
                    Terminal=terminals[i],
                    BerthRemarks=BerthRemarks[i],
                )
            return redirect('addportberth')  # Redirect to a success page
        else:
            # Handle validation error
            return render(request, 'Pages/addPortBerth.html', {'error': 'Please fill all fields.'})

    # Render the form for GET requests
    return render(request, 'Pages/addPortBerth.html')


@login_required
def ExtractData_pg(request):

    ports = Port_Berth_Form.objects.values_list('Port', flat=True).distinct().order_by('Port')
    cargos = SailedData.objects.values_list('Cargo1', flat=True).distinct().order_by('Cargo1')
    sailed_vessel = SailedData.objects.all().order_by('Port', '-ETD_ATD_Date')
    
    context = {
        'ports': ports,
        'cargos':cargos,
        'sailed_Vessel': sailed_vessel,
        'title':'Archived Sailed Vessels'
    }

    return render(request, 'Pages/extractData.html', context)


@login_required
def UpdateLineup_pg(request,id):
    update=LineUpForm.objects.get(id=id)
    data = {
            "ETA_ATA_Date": update.ETA_ATA_Date.strftime("%Y-%m-%d") if update.ETA_ATA_Date else "",
            "ETB_ATB_Date": update.ETB_ATB_Date.strftime("%Y-%m-%d") if update.ETB_ATB_Date else "",
            "ETD_ATD_Date": update.ETD_ATD_Date.strftime("%Y-%m-%d") if update.ETD_ATD_Date else "",
            "ETA_ATA_Time": update.ETA_ATA_Time.strftime("%H:%M") if update.ETA_ATA_Time else "",
            "ETB_ATB_Time": update.ETB_ATB_Time.strftime("%H:%M") if update.ETB_ATB_Time else "",
            "ETD_ATD_Time": update.ETD_ATD_Time.strftime("%H:%M") if update.ETD_ATD_Time else "",
        }
    if request.method=='POST':
        lineup_date=request.POST['lineupdate']
        port=request.POST['port']
        berth=request.POST['berth']
        imo_no=request.POST['imono']
        slt=request.POST['vesselSlt']
        vessel=request.POST['vessel']
        loa=request.POST['loa']
        beam=request.POST['beam']
        draft=request.POST['draft']
        eta_ata_date=request.POST['etadate'] if request.POST['etadate'] else None
        eta_ata_time=request.POST['etatime'] if request.POST['etatime'] else None
        etb_atb_date=request.POST['etbdate'] if request.POST['etbdate'] else None
        etb_atb_time=request.POST['etbtime'] if request.POST['etbtime'] else None
        etd_atd_date=request.POST['etcdate'] if request.POST['etcdate'] else None
        etd_atd_time=request.POST['etctime'] if request.POST['etctime'] else None
        cargo1=request.POST['cargo1']
        cargoqty1=request.POST['cargoqty1']
        cargounits1=request.POST['cargoqtyU1']
        cargo2=request.POST['cargo2']
        cargoqty2=request.POST['cargoqty2']
        cargounits2=request.POST['cargoqtyU2']
        cargo3=request.POST['cargo3']
        cargoqty3=request.POST['cargoqty3']
        cargounits3=request.POST['cargoqtyU3']
        vesseltype=request.POST['vesseltype']
        operations=request.POST['operation']
        shipper=request.POST['shipper']
        receiver=request.POST['receiver']
        principal=request.POST['principal']
        owner=request.POST['owner']
        c_f=request.POST['C/F']
        lastport=request.POST['lastport']
        nextport=request.POST['nextport']
        loadport=request.POST['loadPort']
        dischargeport=request.POST['dischargePort']
        chartereragent=request.POST['cAgent']
        ownersagent=request.POST['agent']
        currentstatus=request.POST['status']
        remarks=request.POST['textarea']
        # updatedAt=request.POST[{current_datetime}]
        

        update.LineUp_Date=lineup_date
        update.Port=port.upper()
        update.Berth=berth
        update.IMO_No=imo_no
        update.Slt=slt
        update.Vessel=vessel.upper()
        update.LOA=loa
        update.Beam=beam
        update.Draft=draft
        update.ETA_ATA_Date=eta_ata_date
        update.ETA_ATA_Time=eta_ata_time
        update.ETB_ATB_Date=etb_atb_date
        update.ETB_ATB_Time=etb_atb_time
        update.ETD_ATD_Date=etd_atd_date
        update.ETD_ATD_Time=etd_atd_time
        update.Cargo1=cargo1.upper()
        update.CargoQty1=cargoqty1
        update.CargoUnits1=cargounits1
        update.Cargo2=cargo2.upper()
        update.CargoQty2=cargoqty2
        update.CargoUnits2=cargounits2
        update.Cargo3=cargo3.upper()
        update.CargoQty3=cargoqty3
        update.CargoUnits3=cargounits3
        update.VesselType=vesseltype
        update.Operations=operations
        update.Shipper=shipper.upper()
        update.Receiver=receiver.upper()
        update.Principal=principal.upper()
        update.Owner=owner.upper()
        update.C_F=c_f
        update.LastPort=lastport.upper()
        update.NextPort=nextport.upper()
        update.LoadPort=loadport.upper()
        update.DischargePort=dischargeport.upper()
        update.ChartererAgent=chartereragent.upper()
        update.OwnersAgent=ownersagent.upper()
        update.CurrentStatus=currentstatus.upper()
        update.Remarks=remarks.upper()
        # update.UpdatedAt=updatedAt
        update.save()
        return redirect('lineupform')


    return render(request, 'Pages/updatelineup.html',{'data': data, 'update': update})


def DeleteLineup_pg(request,id):
    deldata=LineUpForm.objects.get(id=id)
    deldata.delete()
    return redirect('lineupform')

def get_berths(request):
    port = request.GET.get('port')  # Get the selected port from the request
    user_ports = request.session.get('Port', '')

    if not port:
        return JsonResponse({'berths': []})
    
    if request.session.get('UserType') == 'user':
        user_ports = [p.strip() for p in user_ports.split(',')] if user_ports else []
        if port not in user_ports:
            return JsonResponse({'berths': []})
        
        # Fetch all berths for the selected port
    berths = Port_Berth_Form.objects.filter(Port=port).values_list('Berth', flat=True).distinct()

    return JsonResponse({'berths': list(berths)})


def get_updated_berths(request):
    port = request.GET.get('port', None)
    if port:
        # Get unique berths for the selected port
        Uberths = Port_Berth_Form.objects.filter(Port=port).values_list('Berth', flat=True).distinct()
        Uberths_list = list(Uberths)  # Convert QuerySet to a list
        return JsonResponse({'Uberths': Uberths_list})
    return JsonResponse({'Uberths': []})

def get_autocomplete_suggestions(request):
    query = request.GET.get('query', '')  # Get the search term from the URL
    field = request.GET.get('field', '')  # Get the field name from the URL (e.g., 'Shipper', 'Receiver')
    
    if field and hasattr(SailedData, field):  # Check if the field exists in the model
        suggestions = SailedData.objects.filter(**{f"{field}__icontains": query}).values_list(field, flat=True).distinct()
        return JsonResponse(list(suggestions), safe=False)
    else:
        return JsonResponse([], safe=False)
    
####### FILTERING SAILED DATA ######### 
from datetime import datetime
from django.db.models import Q

def filter_sailed_data(request):
    # Start with all objects
    queryset = SailedData.objects.all()
    
    if request.method == 'POST':
        # Get form data
        port = request.POST.get('port')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDatei')
        cargo = request.POST.get('cargo')
        vessel_type = request.POST.get('vesseltype')
        operation = request.POST.get('operation')
        load_port = request.POST.get('loadport')
        discharge_port = request.POST.get('dischargeport')
        agent = request.POST.get('agent')
        
        # Apply filters based on form inputs
        if port:
            queryset = queryset.filter(Port=port)
            
        if start_date and end_date:
            # Convert string dates to date objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(
                Q(ETA_ATA_Date__range=[start_date, end_date]) |
                Q(ETB_ATB_Date__range=[start_date, end_date]) |
                Q(ETD_ATD_Date__range=[start_date, end_date])
            )
            
        if cargo:
            queryset = queryset.filter(
                Q(Cargo1__icontains=cargo) |
                Q(Cargo2__icontains=cargo) |
                Q(Cargo3__icontains=cargo)
            )
            
        if vessel_type:
            queryset = queryset.filter(VesselType__icontains=vessel_type)
            
        if operation:
            queryset = queryset.filter(Operations__icontains=operation)
            
        if load_port:
            queryset = queryset.filter(LoadPort__icontains=load_port)
            
        if discharge_port:
            queryset = queryset.filter(DischargePort__icontains=discharge_port)
            
        if agent:
            queryset = queryset.filter(
                Q(ChartererAgent__icontains=agent) |
                Q(OwnersAgent__icontains=agent)
            )
    
    context = {
        'sailed_data': queryset,
        'ports': ['Port1', 'Port2', 'Port3']  # Replace with your actual ports
    }

    return render(request, 'Pages/extractData.html', context)


from django.http import JsonResponse
from .models import SailedData

def get_vessel_details(request):
    imo_no = request.GET.get('imo', '').strip()
    
    if not imo_no:
        return JsonResponse({'success': False, 'message': 'No IMO provided'})
    
    try:
        vessel = SailedData.objects.filter(IMO_No=imo_no).order_by('-CreatedAt').first()
        
        if vessel:
            return JsonResponse({
                'success': True,
                'vessel': {
                    'slt': vessel.Slt,
                    'name': vessel.Vessel,
                    'loa': str(vessel.LOA),
                    'beam': str(vessel.Beam),
                    'draft': str(vessel.Draft)
                }
            })
        else:
            return JsonResponse({'success': False, 'message': 'No vessel found'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=LineUpForm)
def update_port_last_updated(sender, instance, **kwargs):
    # Update the LastUpdated field in UniquePortDetails whenever LineUpForm is saved
    UniquePortDetails.objects.filter(Port=instance.Port).update(
        LastUpdated=instance.UpdatedAt
    )