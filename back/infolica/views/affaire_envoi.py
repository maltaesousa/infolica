from pyramid.view import view_config
import pyramid.httpexceptions as exc
from sqlalchemy import func, and_
from sqlalchemy.exc import DBAPIError

from .. import models
import transaction
from ..models import Constant
from ..exceptions.custom_error import CustomError
from ..scripts.utils import Utils

import os
from datetime import datetime

import logging
log = logging.getLogger(__name__)


###########################################################
# ENVOIS AFFAIRE
###########################################################

""" GET envois_type"""
@view_config(route_name='envois_types', request_method='GET', renderer='json')
@view_config(route_name='envois_types_s', request_method='GET', renderer='json')
def envois_types_view(request):
    try:
        records = request.dbsession.query(models.EnvoiType).all()
        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" GET envois affaire"""
@view_config(route_name='affaire_envois_by_affaire_id', request_method='GET', renderer='json')
def affaire_envois_view(request):
    affaire_id = request.matchdict['id']

    try:
        records = request.dbsession.query(models.VEnvois)\
            .filter(models.VEnvois.affaire_id == affaire_id).all()

        return Utils.serialize_many(records)

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" POST envois"""
@view_config(route_name='envois', request_method='POST', renderer='json')
@view_config(route_name='envois_s', request_method='POST', renderer='json')
def envois_new_view(request):

    model = models.Envoi()
    model = Utils.set_model_record(model, request.params)

    try:
        with transaction.manager:
            request.dbsession.add(model)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Envoi.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" UPDATE envoi"""
@view_config(route_name='envois', request_method='PUT', renderer='json')
@view_config(route_name='envois_s', request_method='PUT', renderer='json')
def envois_update_view(request):
    
    record_id = request.params['id'] if 'id' in request.params else None
    record = request.dbsession.query(models.Envoi).filter(
        models.Envoi.id == record_id).first()
    
    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Envoi.__tablename__, record_id))

    record = Utils.set_model_record(record, request.params)

    try:
        with transaction.manager:
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_SAVE.format(models.Envoi.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)


""" DELETE envois"""
@view_config(route_name='envois_by_id', request_method='DELETE', renderer='json')
def envois_delete_view(request):
    record_id = request.matchdict['id']

    record = request.dbsession.query(models.Envoi).filter(
        models.Envoi.id == record_id).first()

    if not record:
        raise CustomError(
            CustomError.RECORD_WITH_ID_NOT_FOUND.format(models.Envoi.__tablename__, record_id))

    try:
        with transaction.manager:
            request.dbsession.delete(record)
            transaction.commit()
            return Utils.get_data_save_response(Constant.SUCCESS_DELETE.format(models.Envoi.__tablename__))

    except DBAPIError as e:
        log.error(e)
        return exc.HTTPBadRequest(e)

