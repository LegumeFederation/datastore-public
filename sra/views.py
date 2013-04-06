from os.path import basename, splitext
import logging

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPNotImplemented

from sqlalchemy.exc import DBAPIError

from irods.collection import iRODSCollection
from irods.exception import DataObjectDoesNotExist, CollectionDoesNotExist

from .models import (
    DBSession,
    MyModel,
    DataStoreSession,
)
from .content_types import content_types

#@view_config(route_name='home', renderer='templates/mytemplate.pt')
#def my_view(request):
#    try:
#        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#    except DBAPIError:
#        return Response(conn_err_msg, content_type='text/plain', status_int=500)
#    return {'one': one, 'project': 'sra'}

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {
        'base_url' : '123', 
        'root': request.registry.settings['irods.path'],
        'root_name': basename(request.registry.settings['irods.path']),
        'dir': 'hello',
        'year': '2013'
    }

@view_config(route_name='studies', renderer='json')
def show_studies(request):
    def format_study(study):
        return {
            'id': study.name,
            'path': study.path,
            'url': request.route_path('study', study_id=study.name),
            'title': study.metadata.getone('title')[0],
            'abstract': study.metadata.getone('abstract')[0],
            'description': study.metadata.getone('description')[0] if 'description' in study.metadata else None,
        }

    collection = DataStoreSession.get_collection(request.registry.settings['irods.path'] + '/sra')
    return map(format_study, collection.get_subcollections())

@view_config(route_name='file', renderer='json')
def get_collection(request):
    if not 'path' in request.GET:
        raise HTTPBadRequest()
    path = request.GET['path']
    logging.debug(path)
    collection = DataStoreSession.get_collection(str(path))

    return {
        'name': collection.name,
        'path': collection.path,
        'metadata': [m.__dict__ for m in collection.metadata.items()],
    }

@view_config(route_name='children', renderer='json')
def get_children(request):
    if not 'path' in request.GET:
        raise HTTPBadRequest()
    path = request.GET['path']

    collection = DataStoreSession.get_collection(str(path))
    sub_collections = collection.subcollections
    objects = collection.data_objects
    print sub_collections
    print objects

    def format_subcoll(coll):
        return {
            'name': coll.name,
            'path': coll.path,
            'is_dir': isinstance(coll, iRODSCollection)
        }

    return map(format_subcoll, sub_collections + objects)
    
@view_config(route_name='file_tree')
def file_tree(request):
    if not 'dir' in request.POST:
        raise HTTPBadRequest()
    dir_name = request.POST['dir']
    coll = DataStoreSession.get_collection(dir_name)

    def coll_to_li(coll):
        return '<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (coll.path, coll.name)

    def file_obj_to_li(f):
        ext = splitext(f.name)[1][1:]
        return '<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (ext, f.path, f.name)

    resp = "\n".join(map(coll_to_li, coll.get_subcollections()) + map(file_obj_to_li, coll.get_objects()))
    
    resp = '<ul class="jqueryFileTree" style="display: none;">' + resp + '</ul>'
    return Response(resp)

@view_config(route_name='download_file')
def download_file(request):
    path = request.matchdict['path']
    path = request.registry.settings['irods.path'] + "/" +  "/".join(path)
    try:
        obj = DataStoreSession.get_data_object(str(path))
    except DataObjectDoesNotExist:
        raise HTTPNotFound()

    f = obj.open('r')
    return Response(
        content_disposition='attachment; filename="%s"' % obj.name,
        content_type='application/octet-stream', 
        app_iter=f.read_gen(4096)()
    )

@view_config(route_name='serve_file')
def serve_file(request):
    path = request.matchdict['path']
    path = request.registry.settings['irods.path'] + "/" +  "/".join(path)
    try:
        file = DataStoreSession.get_file(path)
    except FileDoesNotExist:
        raise HTTPNotFound()

    ext = splitext(file.name)[1][1:]

    if ext not in content_types:
        raise HTTPNotImplemented()
    
    return Response(
        content_type=content_types[ext],
        app_iter=file
    )

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_sra_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

