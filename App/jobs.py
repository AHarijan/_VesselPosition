from django.utils import timezone
from .models import LineUpForm, SailedData


def move_sailed_data():
    
    sailed_records = LineUpForm.objects.filter(CurrentStatus="SAILED")
    for record in sailed_records:
        SailedData.objects.create(
            LineUp_Date=record.LineUp_Date,
            Port=record.Port,
            Berth=record.Berth,
            IMO_No=record.IMO_No,
            Slt=record.Slt,
            Vessel=record.Vessel,
            LOA=record.LOA,
            Beam=record.Beam,
            Draft=record.Draft,
            ETA_ATA_Date=record.ETA_ATA_Date,
            ETA_ATA_Time=record.ETA_ATA_Time,
            ETB_ATB_Date=record.ETB_ATB_Date,
            ETB_ATB_Time=record.ETB_ATB_Time,
            ETD_ATD_Date=record.ETD_ATD_Date,
            ETD_ATD_Time=record.ETD_ATD_Time,
            Cargo1=record.Cargo1,
            CargoQty1=record.CargoQty1,
            CargoUnits1=record.CargoUnits1,
            Cargo2=record.Cargo2,
            CargoQty2=record.CargoQty2,
            CargoUnits2=record.CargoUnits2,
            Cargo3=record.Cargo3,
            CargoQty3=record.CargoQty3,
            CargoUnits3=record.CargoUnits3,
            VesselType=record.VesselType,
            Operations=record.Operations,
            Shipper=record.Shipper,
            Receiver=record.Receiver,
            Principal=record.Principal,
            Owner=record.Owner,
            C_F=record.C_F,
            LastPort=record.LastPort,
            NextPort=record.NextPort,
            LoadPort=record.LoadPort,
            DischargePort=record.DischargePort,
            ChartererAgent=record.ChartererAgent,
            OwnersAgent=record.OwnersAgent,
            CurrentStatus=record.CurrentStatus,
            Remarks=record.Remarks,
            CreatedAt=record.CreatedAt,
            UpdatedAt=record.UpdatedAt,
        )
    sailed_records.delete()          


def send_port_update_emails():
    from django.core.mail import send_mail, BadHeaderError
    from smtplib import SMTPException
    import sys
    from datetime import timedelta
    from App.models import UniquePortDetails
    
    now_utc = timezone.now()
    ist_offset = timedelta(hours=5, minutes=30)
    today = (now_utc + ist_offset).date()
    
    ports = UniquePortDetails.objects.filter(LastUpdated__lt=today)

    
    if not ports.exists():
        return "No emails sent - no ports need updates"
    
    email_count = 0
    additional_emails = [
        'alakar.harijan@iss-shipping.com',
        'alakar_harijan@outlook.com'
    ]
    
    for port in ports:
        
        # Build recipient list with validation
        recipient_list = [
            email for email in [
                port.PIC1Mail,
                port.PIC2Mail,
                port.PIC3Mail,
                *additional_emails
            ] if email and isinstance(email, str) and '@' in email
        ]
        
        if not recipient_list:
            continue
        
        # Prepare email content
        try:
            subject = f"LineUp Update Required: {port.Port} ({port.Country})"
            message = f"""
                        Dear Team,

                        Our records show that the information for {port.Port} in {port.Country} hasn't been updated since {port.LastUpdated.strftime('%Y-%m-%d')}.

                        Request you to log in to the lineup system to update lineup for {port.Port}.

                        Thank you,
                        Lineup Management System
                        """
            
            result = send_mail(
                subject=subject,
                message=message,
                from_email='no-reply@iss-shipping.com',
                recipient_list=recipient_list,
                fail_silently=False
            )
            
            if result == 1:
                email_count += 1     
                
        except BadHeaderError:
            print("ERROR: Invalid header found in email content")
        except SMTPException as e:
            print(f"SMTP ERROR: {str(e)}")
        except Exception as e:
            print(f"UNEXPECTED ERROR: {str(e)}")
            print(f"Error type: {sys.exc_info()[0]}")
    
    return f"Sent {email_count} emails"



def send_port_update_missed_emails():
    from django.core.mail import send_mail, BadHeaderError
    from smtplib import SMTPException
    import sys
    from datetime import timedelta
    from App.models import UniquePortDetails
    
    now_utc = timezone.now()
    ist_offset = timedelta(hours=5, minutes=30)
    today = (now_utc + ist_offset).date()
    
    ports = UniquePortDetails.objects.filter(LastUpdated__lt=today)

    
    if not ports.exists():
        return "No emails sent - no ports need updates"
    
    email_count = 0
    additional_emails = [
        'alakar.harijan@iss-shipping.com',
        'alakar_harijan@outlook.com'
    ]
    
    for port in ports:
        
        # Build recipient list with validation
        recipient_list = [
            email for email in [
                port.PIC1Mail,
                port.PIC2Mail,
                port.PIC3Mail,
                *additional_emails
            ] if email and isinstance(email, str) and '@' in email
        ]
        
        if not recipient_list:
            continue
        
        # Prepare email content
        try:
            subject = f"LineUp Update Required: {port.Port} ({port.Country})"
            message = f"""
                        Dear Team,

                        Our records show that the you have missed to update lineup for {port.Port} - {port.Country} on {today}.

                        For tomorrow, please do not forget to update the details for the vessels sailed today i.e. on {today}.

                        Thank you,
                        Lineup Management System
                        """
            
            result = send_mail(
                subject=subject,
                message=message,
                from_email='no-reply@iss-shipping.com',
                recipient_list=recipient_list,
                fail_silently=False
            )
            
            if result == 1:
                email_count += 1     
                
        except BadHeaderError:
            print("ERROR: Invalid header found in email content")
        except SMTPException as e:
            print(f"SMTP ERROR: {str(e)}")
        except Exception as e:
            print(f"UNEXPECTED ERROR: {str(e)}")
            print(f"Error type: {sys.exc_info()[0]}")
    
    return f"Sent {email_count} emails"