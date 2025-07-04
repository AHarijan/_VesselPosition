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


def send_port_update_emails_1():
    from django.core.mail import send_mail, BadHeaderError, EmailMessage
    from smtplib import SMTPException
    import sys
    from datetime import timedelta
    from App.models import UniquePortDetails
    from django.utils import timezone
    
    now_utc = timezone.now()
    ist_offset = timedelta(hours=5, minutes=30)
    today = (now_utc + ist_offset).date()
    
    ports = UniquePortDetails.objects.filter(LastUpdated__lt=today).order_by('Country', 'Port')

    if not ports.exists():
        return "No emails sent - no ports need updates"
    
    # Collect all unique recipients from all ports plus additional emails
    to_recipients = set()
    cc_recipients = set()
    additional_emails = [
        'alakar_harijan@outlook.com'
    ]
    
    for port in ports:
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            to_recipients.add(port.PIC1Mail.lower())
        
        # Add PIC2 and PIC3 to CC field
        if port.PIC2Mail and isinstance(port.PIC2Mail, str) and '@' in port.PIC2Mail:
            cc_recipients.add(port.PIC2Mail.lower())
        if port.PIC3Mail and isinstance(port.PIC3Mail, str) and '@' in port.PIC3Mail:
            cc_recipients.add(port.PIC3Mail.lower())
    
    # Add additional emails
    for email in additional_emails:
        if email and isinstance(email, str) and '@' in email:
            cc_recipients.add(email.lower())
    
    if not to_recipients and not cc_recipients:
        return "No valid recipients found"
    
    # Create the HTML table of ports needing updates
    port_table = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 6px; text-align: left;">Port</th>
                <th style="padding: 6px; text-align: left;">Country</th>
                <th style="padding: 6px; text-align: left;">Last Updated</th>
                <th style="padding: 6px; text-align: left;">Responsible PICs</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for port in ports:
        # Collect PIC emails for this port
        pics = []
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            pics.append(port.PIC1Mail.split('@')[0])
        
        port_table += f"""
        <tr>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Port}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Country}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.LastUpdated.strftime('%Y-%m-%d')}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{', '.join(pics) if pics else 'Not specified'}</td>
        </tr>
        """
    
    port_table += """
        </tbody>
    </table>
    """
    
    # Prepare the email content
    subject = f"LineUp Update Required: {ports.count()} Port{'s' if ports.count() > 1 else ''} Need Updates"
    
    html_message = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ color: #2c3e50; }}
            .footer {{ margin-top: 20px; font-size: 0.9em; color: #7f8c8d; }}
            .highlight {{ background-color: #fffde7; padding: 15px; border-left: 4px solid #ffd600; }}
        </style>
    </head>
    <body>
        <p>Dear Team,</p>
        
        <p>Our records show that the following ports haven't been updated since the dates shown below:</p>
        
        {port_table}
        
        <p>Please log in to the lineup system to update the relevant port information.</p>
        
        <div class="footer">
            <p>Thank you,<br>
            Lineup Management System</p>
            
            <p><em>This is an automated message. Please do not reply directly to this email.</em></p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version for email clients that don't support HTML
    text_message = f"""Dear Team,

Our records show that the following ports haven't been updated recently:

""" + "\n".join([f"- {port.Port} ({port.Country}), last updated: {port.LastUpdated.strftime('%Y-%m-%d')}" for port in ports]) + f"""

Please log in to the lineup system to update the relevant port information.

Thank you,
Lineup Management System

This is an automated message. Please do not reply directly to this email.
"""
    
    try:
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='donot.reply.automail1234@gmail.com',
            to=list(to_recipients),
            cc=list(cc_recipients),
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send(fail_silently=False)
        
        return f"Sent email to {len(to_recipients)} primary recipients (To) and {len(cc_recipients)} secondary recipients (CC) about {ports.count()} ports"
        
    except BadHeaderError:
        return "ERROR: Invalid header found in email content"
    except SMTPException as e:
        return f"SMTP ERROR: {str(e)}"
    except Exception as e:
        return f"UNEXPECTED ERROR: {str(e)}"
    

def send_port_update_emails_2():
    from django.core.mail import send_mail, BadHeaderError, EmailMessage
    from smtplib import SMTPException
    import sys
    from datetime import timedelta
    from App.models import UniquePortDetails
    from django.utils import timezone
    
    now_utc = timezone.now()
    ist_offset = timedelta(hours=5, minutes=30)
    today = (now_utc + ist_offset).date()
    
    ports = UniquePortDetails.objects.filter(LastUpdated__lt=today).order_by('Country', 'Port')

    if not ports.exists():
        return "No emails sent - no ports need updates"
    
    # Collect all unique recipients from all ports plus additional emails
    to_recipients = set()
    cc_recipients = set()
    additional_emails = [
        'alakar_harijan@outlook.com'
    ]
    
    for port in ports:
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            to_recipients.add(port.PIC1Mail.lower())
        
        # Add PIC2 and PIC3 to CC field
        if port.PIC2Mail and isinstance(port.PIC2Mail, str) and '@' in port.PIC2Mail:
            cc_recipients.add(port.PIC2Mail.lower())
        if port.PIC3Mail and isinstance(port.PIC3Mail, str) and '@' in port.PIC3Mail:
            cc_recipients.add(port.PIC3Mail.lower())
    
    # Add additional emails
    for email in additional_emails:
        if email and isinstance(email, str) and '@' in email:
            cc_recipients.add(email.lower())
    
    if not to_recipients and not cc_recipients:
        return "No valid recipients found"
    
    # Create the HTML table of ports needing updates
    port_table = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 6px; text-align: left;">Port</th>
                <th style="padding: 6px; text-align: left;">Country</th>
                <th style="padding: 6px; text-align: left;">Last Updated</th>
                <th style="padding: 6px; text-align: left;">Responsible PICs</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for port in ports:
        # Collect PIC emails for this port
        pics = []
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            pics.append(port.PIC1Mail.split('@')[0])
        
        port_table += f"""
        <tr>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Port}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Country}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.LastUpdated.strftime('%Y-%m-%d')}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{', '.join(pics) if pics else 'Not specified'}</td>
        </tr>
        """
    
    port_table += """
        </tbody>
    </table>
    """
    
    # Prepare the email content
    subject = f"LineUp Update Required: {ports.count()} Port{'s' if ports.count() > 1 else ''} Need Updates"
    
    html_message = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ color: #2c3e50; }}
            .footer {{ margin-top: 20px; font-size: 0.9em; color: #7f8c8d; }}
            .highlight {{ background-color: #fffde7; padding: 15px; border-left: 4px solid #ffd600; }}
        </style>
    </head>
    <body>
        <p>Dear Team,</p>
        
        <p>Our records show that the following ports haven't been updated since the dates shown below:</p>
        
        {port_table}
        
        <p>Please log in to the lineup system to update the relevant port information.</p>
        
        <div class="footer">
            <p>Thank you,<br>
            Lineup Management System</p>
            
            <p><em>This is an automated message. Please do not reply directly to this email.</em></p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version for email clients that don't support HTML
    text_message = f"""Dear Team,

Our records show that the following ports haven't been updated recently:

""" + "\n".join([f"- {port.Port} ({port.Country}), last updated: {port.LastUpdated.strftime('%Y-%m-%d')}" for port in ports]) + f"""

Please log in to the lineup system to update the relevant port information.

Thank you,
Lineup Management System

This is an automated message. Please do not reply directly to this email.
"""
    
    try:
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='donot.reply.automail1234@gmail.com',
            to=list(to_recipients),
            cc=list(cc_recipients),
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send(fail_silently=False)
        
        return f"Sent email to {len(to_recipients)} primary recipients (To) and {len(cc_recipients)} secondary recipients (CC) about {ports.count()} ports"
        
    except BadHeaderError:
        return "ERROR: Invalid header found in email content"
    except SMTPException as e:
        return f"SMTP ERROR: {str(e)}"
    except Exception as e:
        return f"UNEXPECTED ERROR: {str(e)}"
    


def send_port_update_emails_3():
    from django.core.mail import send_mail, BadHeaderError, EmailMessage
    from smtplib import SMTPException
    import sys
    from datetime import timedelta
    from App.models import UniquePortDetails
    from django.utils import timezone
    
    now_utc = timezone.now()
    ist_offset = timedelta(hours=5, minutes=30)
    today = (now_utc + ist_offset).date()
    
    ports = UniquePortDetails.objects.filter(LastUpdated__lt=today).order_by('Country', 'Port')

    if not ports.exists():
        return "No emails sent - no ports need updates"
    
    # Collect all unique recipients from all ports plus additional emails
    to_recipients = set()
    cc_recipients = set()
    additional_emails = [
        'alakar_harijan@outlook.com'
    ]
    
    for port in ports:
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            to_recipients.add(port.PIC1Mail.lower())
        
        # Add PIC2 and PIC3 to CC field
        if port.PIC2Mail and isinstance(port.PIC2Mail, str) and '@' in port.PIC2Mail:
            cc_recipients.add(port.PIC2Mail.lower())
        if port.PIC3Mail and isinstance(port.PIC3Mail, str) and '@' in port.PIC3Mail:
            cc_recipients.add(port.PIC3Mail.lower())
    
    # Add additional emails
    for email in additional_emails:
        if email and isinstance(email, str) and '@' in email:
            cc_recipients.add(email.lower())
    
    if not to_recipients and not cc_recipients:
        return "No valid recipients found"
    
    # Create the HTML table of ports needing updates
    port_table = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 6px; text-align: left;">Port</th>
                <th style="padding: 6px; text-align: left;">Country</th>
                <th style="padding: 6px; text-align: left;">Last Updated</th>
                <th style="padding: 6px; text-align: left;">Responsible PICs</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for port in ports:
        # Collect PIC emails for this port
        pics = []
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            pics.append(port.PIC1Mail.split('@')[0])
        
        port_table += f"""
        <tr>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Port}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Country}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.LastUpdated.strftime('%Y-%m-%d')}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{', '.join(pics) if pics else 'Not specified'}</td>
        </tr>
        """
    
    port_table += """
        </tbody>
    </table>
    """
    
    # Prepare the email content
    subject = f"LineUp Update Required: {ports.count()} Port{'s' if ports.count() > 1 else ''} Need Updates"
    
    html_message = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ color: #2c3e50; }}
            .footer {{ margin-top: 20px; font-size: 0.9em; color: #7f8c8d; }}
            .highlight {{ background-color: #fffde7; padding: 15px; border-left: 4px solid #ffd600; }}
        </style>
    </head>
    <body>
        <p>Dear Team,</p>
        
        <p>Our records show that the following ports haven't been updated since the dates shown below:</p>
        
        {port_table}
        
        <p>Please log in to the lineup system to update the relevant port information.</p>
        
        <div class="footer">
            <p>Thank you,<br>
            Lineup Management System</p>
            
            <p><em>This is an automated message. Please do not reply directly to this email.</em></p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version for email clients that don't support HTML
    text_message = f"""Dear Team,

Our records show that the following ports haven't been updated recently:

""" + "\n".join([f"- {port.Port} ({port.Country}), last updated: {port.LastUpdated.strftime('%Y-%m-%d')}" for port in ports]) + f"""

Please log in to the lineup system to update the relevant port information.

Thank you,
Lineup Management System

This is an automated message. Please do not reply directly to this email.
"""
    
    try:
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='donot.reply.automail1234@gmail.com',
            to=list(to_recipients),
            cc=list(cc_recipients),
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send(fail_silently=False)
        
        return f"Sent email to {len(to_recipients)} primary recipients (To) and {len(cc_recipients)} secondary recipients (CC) about {ports.count()} ports"
        
    except BadHeaderError:
        return "ERROR: Invalid header found in email content"
    except SMTPException as e:
        return f"SMTP ERROR: {str(e)}"
    except Exception as e:
        return f"UNEXPECTED ERROR: {str(e)}"
    

def send_port_update_missed_emails():
    from django.core.mail import send_mail, BadHeaderError, EmailMessage
    from smtplib import SMTPException
    import sys
    from datetime import timedelta
    from App.models import UniquePortDetails
    from django.utils import timezone
    
    now_utc = timezone.now()
    ist_offset = timedelta(hours=5, minutes=30)
    today = (now_utc + ist_offset).date()
    
    ports = UniquePortDetails.objects.filter(LastUpdated__lt=today).order_by('Country', 'Port')

    if not ports.exists():
        return "No emails sent - no ports need updates"
    
    # Collect all unique recipients from all ports plus additional emails
    to_recipients = set()
    cc_recipients = set()
    additional_emails = [
        'alakar_harijan@outlook.com'
    ]
    
    for port in ports:
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            to_recipients.add(port.PIC1Mail.lower())
        
        # Add PIC2 and PIC3 to CC field
        if port.PIC2Mail and isinstance(port.PIC2Mail, str) and '@' in port.PIC2Mail:
            cc_recipients.add(port.PIC2Mail.lower())
        if port.PIC3Mail and isinstance(port.PIC3Mail, str) and '@' in port.PIC3Mail:
            cc_recipients.add(port.PIC3Mail.lower())
    
    # Add additional emails
    for email in additional_emails:
        if email and isinstance(email, str) and '@' in email:
            cc_recipients.add(email.lower())
    
    if not to_recipients and not cc_recipients:
        return "No valid recipients found"
    
    # Create the HTML table of ports needing updates
    port_table = """
    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 6px; text-align: left;">Port</th>
                <th style="padding: 6px; text-align: left;">Country</th>
                <th style="padding: 6px; text-align: left;">Last Updated</th>
                <th style="padding: 6px; text-align: left;">Responsible PICs</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for port in ports:
        # Collect PIC emails for this port
        pics = []
        if port.PIC1Mail and isinstance(port.PIC1Mail, str) and '@' in port.PIC1Mail:
            pics.append(port.PIC1Mail.split('@')[0])
        
        port_table += f"""
        <tr>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Port}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.Country}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{port.LastUpdated.strftime('%Y-%m-%d')}</td>
            <td style="padding: 6px; border-bottom: 1px solid #ddd;">{', '.join(pics) if pics else 'Not specified'}</td>
        </tr>
        """
    
    port_table += """
        </tbody>
    </table>
    """
    
    # Prepare the email content
    subject = f"LineUp Update Required: {ports.count()} Port{'s' if ports.count() > 1 else ''} Need Updates"
    
    html_message = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ color: #2c3e50; }}
            .footer {{ margin-top: 20px; font-size: 0.9em; color: #7f8c8d; }}
            .highlight {{ background-color: #fffde7; padding: 15px; border-left: 4px solid #ffd600; }}
        </style>
    </head>
    <body>
        <p>Dear Team,</p>
        
        <p>Our records show that vessel lineup for the following ports haven't been updated today:</p>
        
        {port_table}
        
        <p>We request you, tomorrow please update the vessels that have sailed out today.</p>
        
        <div class="footer">
            <p>Thank you,<br>
            Lineup Management System</p>
            
            <p><em>This is an automated message. Please do not reply directly to this email.</em></p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version for email clients that don't support HTML
    text_message = f"""Dear Team,

Our records show that the following ports haven't been updated recently:

""" + "\n".join([f"- {port.Port} ({port.Country}), last updated: {port.LastUpdated.strftime('%Y-%m-%d')}" for port in ports]) + f"""

Please log in to the lineup system to update the relevant port information.

Thank you,
Lineup Management System

This is an automated message. Please do not reply directly to this email.
"""
    
    try:
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email='donot.reply.automail1234@gmail.com',
            to=list(to_recipients),
            cc=list(cc_recipients),
        )
        email.content_subtype = "html"  # Set content type to HTML
        email.send(fail_silently=False)
        
        return f"Sent email to {len(to_recipients)} primary recipients (To) and {len(cc_recipients)} secondary recipients (CC) about {ports.count()} ports"
        
    except BadHeaderError:
        return "ERROR: Invalid header found in email content"
    except SMTPException as e:
        return f"SMTP ERROR: {str(e)}"
    except Exception as e:
        return f"UNEXPECTED ERROR: {str(e)}"
