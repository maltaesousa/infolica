from pyramid.view import view_config
import pyramid.httpexceptions as exc
from ..scripts.utils import Utils
from ..models import Constant
import transaction

from sqlalchemy.exc import DBAPIError
from ..exceptions.custom_error import CustomError

from .. import models

import logging
log = logging.getLogger(__name__)


""" Return all suivis_mandats"""
@view_config(route_name='suivis_mandats', request_method='GET', renderer='json')
@view_config(route_name='suivis_mandats_s', request_method='GET', renderer='json')
def suivis_mandats_view(request):
    try:
        query = request.dbsession.query(models.SuiviMandat).all()
        return Utils.serialize_many(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Return suivis_mandats by id"""
@view_config(route_name='suivi_mandat_by_id', request_method='GET', renderer='json')
def suivis_mandats_by_id_view(request):
    try:
        # Get controle mutation id
        id = request.id = request.matchdict['id']
        query = request.dbsession.query(models.SuiviMandat).filter(
            models.SuiviMandat.id == id).first()
        return Utils.serialize_one(query)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Add new suivis_mandats"""
@view_config(route_name='suivis_mandats', request_method='POST', renderer='json')
@view_config(route_name='suivis_mandats_s', request_method='POST', renderer='json')
def suivis_mandats_new_view(request):

    record = models.SuiviMandat()
    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(record)
            request.dbsession.flush()
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.SuiviMandat.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Update suivis_mandats"""
@view_config(route_name='suivis_mandats', request_method='PUT', renderer='json')
@view_config(route_name='suivis_mandats_s', request_method='PUT', renderer='json')
def suivis_mandats_update_view(request):

    # Get controle mutation id
    id = request.params['id'] if 'id' in request.params else None

    # Get controle mutation record
    record = request.dbsession.query(models.SuiviMandat).filter(
        models.SuiviMandat.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.SuiviMandat.__tablename__, id))

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.SuiviMandat.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" Delete suivis_mandats"""
@view_config(route_name='suivis_mandats', request_method='DELETE', renderer='json')
@view_config(route_name='suivis_mandats_s', request_method='DELETE', renderer='json')
def suivis_mandats_delete_view(request):

    # Get controle mutation id
    id = request.params['id'] if 'id' in request.params else None

    # Get controle mutation record
    record = request.dbsession.query(models.SuiviMandat).filter(
        models.SuiviMandat.id == id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.SuiviMandat.__tablename__, id))

    try:
        with transaction.manager:
            request.dbsession.delete(record)
            # Commit transaction
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.SuiviMandat.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)
