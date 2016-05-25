from irods.session import iRODSSession
from . import settings


DataStoreSession = iRODSSession()
DataStoreSession.configure(
    host=settings.irods['host'],
    port=int(settings.irods['port']),
    zone=settings.irods['zone'],
    user=settings.irods['user'],
    password=settings.irods['password']
)
