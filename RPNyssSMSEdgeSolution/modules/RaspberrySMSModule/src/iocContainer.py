
import logging
import sqlite3
from smshandling.smsService import SmsService
from publishing.services import ApiPublisher
import main
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from gsm import create_gsmadapter
from sqlalchemy.pool import StaticPool
import sys
import os


def initialize(config):
    logger = logging.getLogger("NYSS-Gateway")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    database_engine = create_engine(config['database']['url'], connect_args={
                                    'check_same_thread': False})

    needToCreateDatabase = False
    if os.path.exists(config['database']['file']) is False:
        needToCreateDatabase = True
    if needToCreateDatabase:
        main.createDatabase(engine=database_engine)

    session_maker = sessionmaker(bind=database_engine)

    session_factory = scoped_session(session_maker)

    sms_service = SmsService(logger=logger, sessionFactory=session_factory)

    gsm_adapter = create_gsmadapter(
        reader_type=config['gsm']['handler'], smsService=sms_service, logger=logger)

    api_publisher = ApiPublisher(API_URL=config['api']['url'],
                                 API_ID=config['api']['id'],
                                 API_KEY=config['api']['key'],
                                 logger=logger,
                                 smsService=sms_service)

    main.main(sms_service)

