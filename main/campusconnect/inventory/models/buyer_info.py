from django.db import models


class BuyerInfoModel(models.Model):
    purchase_id   = models.CharField(max_length=300, default="00000000000")
    email_address = models.CharField(max_length=300)
    buyer_type    = models.CharField(max_length=20)
    
    created       = models.DateTimeField(auto_now_add=True, help_text="timestamp of creation")
    updated       = models.DateTimeField(auto_now=True, help_text="timestamp of last update")

    class Meta:
        verbose_name 		= 'Buyer Info'
        verbose_name_plural = 'Buyer Info'

    def __str__(self):
        return "{}->{}".format(self.purchase_id, self.email_address)
