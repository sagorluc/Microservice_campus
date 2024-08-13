from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone

# from systemops import check_order_progress_status


def get_users_purchase_history(email):
    data_list = []
    
    # Get a list of mcompleted_purchase_ids associated with the given email
    mcompleted_purchase_ids = BuyerInfoModel.objects.filter(email_address=email).values_list("purchase_id", flat=True)
    
    # Retrieve mcart objects based on mcompleted_purchase_ids
    for purid in mcompleted_purchase_ids:
        data_list.append(mcart.objects.filter(mcompleted_purchase=purid))

    return data_list


def get_mcart_basic_info(tracking_id):
    mcart_objects = mcart.objects.filter(tracking_id=tracking_id)
    return {
        'tracking_id': mcart_objects.values_list("tracking_id", flat=True),
        'created': mcart_objects.values_list("created", flat=True),
        'title': mcart_objects.values_list("title", flat=True),
        'sku': mcart_objects.values_list("sku", flat=True),
        'final_price': mcart_objects.values_list("final_price", flat=True),
        'processing_status': mcart_objects.values_list("processing_status", flat=True),
        'mcart_id': mcart_objects.values_list("id", flat=True),
    }

def get_mcart_service_options(mcart_id):
    return mcart_serviceoptions.objects.filter(mcart_id=mcart_id)

def get_mcart_delivery_options(mcart_id):
    return mcart_deliveryoptions.objects.filter(mcart_id=mcart_id)

def calculate_grace_period(purshased_order_list_sorted):
    value_temp = list([i['created'] for i in purshased_order_list_sorted])[0]
    value_temp = value_temp[0]
    value_temp = value_temp.replace(tzinfo=timezone.utc)
    # print("value_temp {}".format(value_temp))

    # # Check if value_temp is offset-naive
    # if value_temp.tzinfo is None:
    #     print("value_temp is offset-naive (without timezone information)")
    # else:
    #     print("value_temp is offset-aware (with timezone information)")

    # Calculate the time difference
    time_difference = datetime.now(timezone.utc) - value_temp
    # Compare with timedelta representing 24 hours
    is_more_than_24_hours_ago = time_difference > timedelta(hours=24)

    if is_more_than_24_hours_ago:
        # print("The datetime is more than 24 hours ago.")
        check_grace_period = False
    else:
        # print("The datetime is within the last 24 hours.")
        check_grace_period = True

    # print("check_grace_period {}".format(check_grace_period))
    return check_grace_period

def get_purchased_order_data(tracking_ids, request):
    data = []
    
    for var in tracking_ids:
        purchase_data_dict = get_mcart_basic_info(var)
        
        purchase_data_dict['service_options'] = get_mcart_service_options(purchase_data_dict['mcart_id'][0])
        purchase_data_dict['delivery_options'] = get_mcart_delivery_options(purchase_data_dict['mcart_id'][0])
        # purchase_data_dict['delivery_status'] = get_mcart_delivery_status(var)

        order_progress_status = check_order_progress_status(request.user.email, purchase_data_dict['tracking_id'])
        if order_progress_status:
            order_progress_status_value = order_progress_status[0].get("order_progress", 5)
            purchase_data_dict['order_progress_status'] = int(order_progress_status_value)
        else:
            purchase_data_dict['order_progress_status'] = 5

        data.append(purchase_data_dict)

    return data
