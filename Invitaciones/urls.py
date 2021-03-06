from django.urls import path


from .views import *

"""path


    Args:
        route: URL pattern.
        view: view function
        kwargs: Adittional arguments to pass a view function or method.
        name:  Used for pick the URL pattern out of application.
    route   
"""
urlpatterns = [
    # Obtiene la invitacion
    path('get_inv/<year>/<month>/<day>/', InvitationListAdminEmployee.as_view({'get': 'list'}), name='get_invitations_url'),  # path(route, view, kwargs, name= None)]
    # Obtiene las invitaciones del Usuario (INVITADO)
    path('get_inv/user', InvitationListToSimpleUser.as_view({'get': 'list'}), name='get_inv_user'), #
    # Crea Invitaciones ya sea individuales o Masivamanete
    path('create_inv/', MassiveInvitationCreate.as_view(), name='create_invitations_url'),  # path(route, view, kwargs, name= None
    # Obtiene la invitacion por codigo QR
    path('get_inv/qr/<qrcode>/', InvitationbyQRCode.as_view(), name='getInv_qrCode'),  # Get only one invitation by QR_CODE
    # Obtiene los datos de la Invitación por ID_INVITACION
    path('get_inv/<int:pk>', InvitationListToManagerAndEmployee.as_view({'get': 'list'}), name='getInv_byID'),
    # Obtiene la invitacion por Codigo QR especialemente prestanda para el GUARDIA
    path('get_inv/gaurd/<str:qr_code>/', InvitationListToGuard.as_view({'get': 'list'}), name='get_inv_qrcode_guard'),
    path('create_massiveInv/', MassiveInvitationCreate.as_view()),
    #Regresa todas las Invitaciones hechas ya sea por un Administrador o por un Empleado
    path('getInv/Admin/Employee/', GetInvitationByHOST.as_view({'get': 'list'})),
    path('createReferred/Inv/', Createreferredinvitation.as_view()),
    # Obtiene invitacion empresarial mediante un Token
    path('getReferralInv/<str:token>/', GetReferredInv.as_view({'get': 'list'})),
    # Creacion Invitacion Empresarial
    path('createReferredInv', Createreferredinvitation.as_view()),
    path('createEnterpriseInv', CreateEnterpriseInvitation.as_view()),
    # Elimina una invitacion
    path('deleteInvitation/<int:pk>/', DeleteInvitation.as_view()),
    # Concertar Invitacion(Invitado confirma que asistirá a la cita)
    path('setConfirmed_Appointment/<str:qr_code>/<flag>/', SetConfirmAppointment.as_view()),
    path('setConfirmed_AppointmentFromMail/<str:qr_code>/<flag>/', SetConfirmAppointmentFromMail.as_view()),
    path ('updateTimeInvitation/<str:qr_code>/', UpdateTimeInvitation.as_view()),
    path('get_invByDateRange/<year1>/<month1>/<day1>/<year2>/<month2>/<day2>/',
         InvitationListAdminEmployeeByRangeDate.as_view({'get': 'list'})),
    path('get_inv/userByDateRange/<year1>/<month1>/<day1>/<year2>/<month2>/<day2>/',
         InvitationListToSimpleUserByDateRange.as_view({'get': 'list'}), name='get_inv_user'),
]
