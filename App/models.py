from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    port = models.CharField(max_length=50, default="")
    country = models.CharField(max_length=50, default="")
    email = models.EmailField(unique=True, default="")
    CombinedField = models.CharField(max_length=90, default="")
    usertype = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.username

####### MODEL FOR RESETTING PASSWORD #######
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.CustomUser.username} at {self.created_when}" 

####### MODEL FOR ENTERING LINEUP DATA #######
class LineUpForm(models.Model):
    LineUp_Date=models.CharField(max_length=20,default="")
    Port=models.CharField(max_length=20,default="")
    Berth=models.CharField(max_length=20,default="")
    IMO_No=models.CharField(max_length=20,default="")
    Slt=models.CharField(max_length=20,default="")
    Vessel=models.CharField(max_length=20,default="")
    LOA=models.DecimalField(max_digits=20,decimal_places=2)
    Beam=models.DecimalField(max_digits=20,decimal_places=2)
    Draft=models.DecimalField(max_digits=20,decimal_places=2)
    ETA_ATA_Date=models.DateField(null=True, blank=True)
    ETA_ATA_Time=models.TimeField(null=True, blank=True)
    ETB_ATB_Date=models.DateField(null=True, blank=True)
    ETB_ATB_Time=models.TimeField(null=True, blank=True)
    ETD_ATD_Date=models.DateField(null=True, blank=True)
    ETD_ATD_Time=models.TimeField(null=True, blank=True)
    Cargo1=models.CharField(max_length=20,default="")
    CargoQty1=models.DecimalField(max_digits=20,decimal_places=2)
    CargoUnits1=models.CharField(max_length=20,default="")
    Cargo2=models.CharField(max_length=20,default="")
    CargoQty2=models.DecimalField(max_digits=20,decimal_places=2)
    CargoUnits2=models.CharField(max_length=20,default="")
    Cargo3=models.CharField(max_length=20,default="")
    CargoQty3=models.DecimalField(max_digits=20,decimal_places=2)
    CargoUnits3=models.CharField(max_length=20,default="")
    VesselType=models.CharField(max_length=20,default="")
    Operations=models.CharField(max_length=20,default="")
    Shipper=models.CharField(max_length=20,default="")
    Receiver=models.CharField(max_length=20,default="")
    Principal=models.CharField(max_length=20,default="")
    Owner=models.CharField(max_length=20,default="")
    C_F=models.CharField(max_length=20,default="")
    LastPort=models.CharField(max_length=20,default="")
    NextPort=models.CharField(max_length=20,default="")
    LoadPort=models.CharField(max_length=20,default="")
    DischargePort=models.CharField(max_length=20,default="")
    ChartererAgent=models.CharField(max_length=20,default="")
    OwnersAgent=models.CharField(max_length=20,default="")
    CurrentStatus=models.CharField(max_length=20,default="")
    Remarks=models.CharField(max_length=200,default="")
    CreatedAt=models.DateTimeField(auto_now_add=True)
    UpdatedAt=models.DateTimeField(auto_now=True)


class SailedData(models.Model):
    LineUp_Date=models.CharField(max_length=20,default="")
    Port=models.CharField(max_length=20,default="")
    Berth=models.CharField(max_length=20,default="")
    IMO_No=models.CharField(max_length=20,default="")
    Slt=models.CharField(max_length=20,default="")
    Vessel=models.CharField(max_length=20,default="")
    LOA=models.DecimalField(max_digits=20,decimal_places=2)
    Beam=models.DecimalField(max_digits=20,decimal_places=2)
    Draft=models.DecimalField(max_digits=20,decimal_places=2)
    ETA_ATA_Date=models.DateField(null=True, blank=True)
    ETA_ATA_Time=models.TimeField(null=True, blank=True)
    ETB_ATB_Date=models.DateField(null=True, blank=True)
    ETB_ATB_Time=models.TimeField(null=True, blank=True)
    ETD_ATD_Date=models.DateField(null=True, blank=True)
    ETD_ATD_Time=models.TimeField(null=True, blank=True)
    Cargo1=models.CharField(max_length=20,default="")
    CargoQty1=models.DecimalField(max_digits=20,decimal_places=2)
    CargoUnits1=models.CharField(max_length=20,default="")
    Cargo2=models.CharField(max_length=20,default="")
    CargoQty2=models.DecimalField(max_digits=20,decimal_places=2)
    CargoUnits2=models.CharField(max_length=20,default="")
    Cargo3=models.CharField(max_length=20,default="")
    CargoQty3=models.DecimalField(max_digits=20,decimal_places=2)
    CargoUnits3=models.CharField(max_length=20,default="")
    VesselType=models.CharField(max_length=20,default="")
    Operations=models.CharField(max_length=20,default="")
    Shipper=models.CharField(max_length=20,default="")
    Receiver=models.CharField(max_length=20,default="")
    Principal=models.CharField(max_length=20,default="")
    Owner=models.CharField(max_length=20,default="")
    C_F=models.CharField(max_length=20,default="")
    LastPort=models.CharField(max_length=20,default="")
    NextPort=models.CharField(max_length=20,default="")
    LoadPort=models.CharField(max_length=20,default="")
    DischargePort=models.CharField(max_length=20,default="")
    ChartererAgent=models.CharField(max_length=20,default="")
    OwnersAgent=models.CharField(max_length=20,default="")
    CurrentStatus=models.CharField(max_length=20,default="")
    Remarks=models.CharField(max_length=200,default="")    
    CreatedAt=models.DateTimeField(null=True, blank=True)
    UpdatedAt=models.DateTimeField(null=True, blank=True)

class UniquePortDetails(models.Model):
    Country = models.CharField(max_length=20, default="")
    Port = models.CharField(max_length=20, default="", unique=True)
    PIC1Mail = models.EmailField(max_length=30, default="")
    PIC2Mail = models.EmailField(max_length=30, default="")
    PIC3Mail = models.EmailField(max_length=30, default="")
    LastUpdated = models.DateField(null=True, blank=True)
    

    class Meta:
        verbose_name = "Unique Port Detail"
        verbose_name_plural = "Unique Port Details"

    def __str__(self):
        return f"{self.Port}, {self.Country}"

class Port_Berth_Form(models.Model):
    Country = models.CharField(max_length=20, default="")
    Port = models.CharField(max_length=20, default="")
    PIC1Mail = models.EmailField(max_length=30, default="")
    PIC2Mail = models.EmailField(max_length=30, default="")
    PIC3Mail = models.EmailField(max_length=30, default="")
    Berth = models.CharField(max_length=20, default="")
    Cargos_Handled_on_Berth = models.CharField(max_length=200, default="")
    Terminal = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name = "Port Berth Form"
        verbose_name_plural = "Port Berth Forms"

    def __str__(self):
        return f"{self.Port} - {self.Berth}"

    def save(self, *args, **kwargs):
        # First save the Port_Berth_Form instance
        super().save(*args, **kwargs)
        
        # Then update or create the corresponding UniquePortDetails entry
        UniquePortDetails.objects.update_or_create(
            Port=self.Port,
            defaults={
                'Country': self.Country,
                'PIC1Mail': self.PIC1Mail,
                'PIC2Mail': self.PIC2Mail,
                'PIC3Mail': self.PIC3Mail
            }
        )