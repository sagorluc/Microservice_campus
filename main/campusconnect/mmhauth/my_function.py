
import logging
logger = logging.getLogger(__name__)


def user_is_deactivated(email):
    # query through Deactivateacc model & pass email
    # model = DeactivatedAccount
    # model_email = DeactivatedAccount.objects.filter(email=formemail).first()
    mmk = DeactivatedAccountModel.objects.filter(email=email).exists()
    
    if mmk:
        logger.warning("calling user_is_deactivated ")
        return True
    else: 
    	return False

