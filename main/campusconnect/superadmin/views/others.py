from zzz_lib.zzz_log import zzz_print
from django.contrib import admin

from guestactions.models import (
    GuestResumeModel,
    SiteSurveyModel,
    ContactUsModel,
    InviteFriendsModel,
)

#from guestactions.models.guest_resume_upload import GuestResumeModel

from mymailroom.models import (
    msendmail,
)

from inventory.models import BuyerInfoModel

from inventory.models.mssl_commerz import mssl_commerz

@admin.register(mssl_commerz)
class AdminSSL_commerz(admin.ModelAdmin):
    list_display = (
        "id",
    )

@admin.register(msendmail)
class Adminmsendmail(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
    )


@admin.register(GuestResumeModel)
class admin_GuestResumeFiles(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "file1",
        "upload_time",
    )
    
@admin.register(BuyerInfoModel)
class admin_BuyerInfoModel(admin.ModelAdmin):
    list_display = (
        "purchase_id",
        "email_address",
        "buyer_type",
        
    )
    
@admin.register(InviteFriendsModel)
class admin_InviteFriendsModel(admin.ModelAdmin):
    list_display = (
        "guest_first_name",
        "guest_email_address",
        "friend_first_name",
        "friend_email_address",
        
    )


@admin.register(SiteSurveyModel)
class AdminSiteSurvey(admin.ModelAdmin):
    list_display = (
        "id",
        "created_at"
    )

