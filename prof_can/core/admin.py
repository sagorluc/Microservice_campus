from django.contrib import admin
from core.models.cust_comm import CandidateInternalMsg
from core.models.disputes import DisputeSubmissionModel
from core.models.resume_profile import (ResumeDocType, ResumeFormType)
from core.models.acc_sett import DeactivatedAccountModel
from core.models.order_feedback import OrderFeedbackModel
from core.models.order_cancellation import OrderCancellationRequest

class CandidateInternalMsgAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'msg']
    ordering = ['-id']
    
class DisputeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'submission_id', 'message']
    ordering = ['-id']
    
class ResumeDocTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'document', 'deleted']
    ordering = ['-id']
    
class ResumeFormTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'Exp_1', 'Exp_2']
    ordering = ['-id']
    
class DeactivatedAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'confirmation']
    ordering = ['-id']
    
class OrderFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'submited_by']
    ordering = ['-id']
    
class OrderCancellationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'created_for', 'submitted_by']
    ordering = ['-id']
    
    
admin.site.register(CandidateInternalMsg, CandidateInternalMsgAdmin)
admin.site.register(DisputeSubmissionModel, DisputeSubmissionAdmin)
admin.site.register(ResumeDocType, ResumeDocTypeAdmin)
admin.site.register(ResumeFormType, ResumeFormTypeAdmin)
admin.site.register(DeactivatedAccountModel, DeactivatedAccountAdmin)
admin.site.register(OrderFeedbackModel, OrderFeedbackAdmin)
admin.site.register(OrderCancellationRequest, OrderCancellationRequestAdmin)