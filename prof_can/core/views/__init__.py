from .home import (
    CandidateProfileHome,
    MemberBenefitsView
)

from .my_orders import (
    MyOrderHistoryView,
    OrderDetailsView,
    # MyInvoices,
    # InvoicePDF,
    # mmh: removed when processing merged into pending view
    # OrderHistoryInProcessing,
)

from .my_resume_download import (
    resume_download_view,
)

from .order_cancellation import (
    CancelOrder_mmh,
    CancelOrderSuccess_mmh,
    CancellationDetailsView,
    # CancelOrderFailed_mmh,
    OrderCancellationRequestView,
    OrderCancellationConfirmationView,
    OrderCancelHistoryAll,

)

from .dispute import (
    SubmitDisputeView,
    DisputeHistoryView,
    DisputeDetailsView,
    DisputeResultView,
    # DisputeConfirmation,
    # SubmitDisputeFromOrderDetails,

)

from .order_feedback import OrderFeedbackSubmitView

from .my_resume import (
    ResumeDocView,
    ResumeFormView,
    ResumeFormEditView,
    ResumeFormTips,
    ResumeFormConfirm,
    delete_doc,
    
)


from .cust_comm import (
    CandidateMsg,
    MsgHistory,
    MsgDetails,
    MsgConfirm,
)


from .rewards import (
    MyCurrentRewardOffers,
    MyEarnedCoupons,

)


from .acct_set import (
    AcctSettingsHomeView,
    UpdatePassView,
    SubmitAccountDeactivateView,
    AccDeactivateConfirmView,
    
)
