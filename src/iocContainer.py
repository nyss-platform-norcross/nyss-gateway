from dependency_injector import containers, providers

import logging
import sqlite3
from smshandling.smsService import SmsService
from publishing.services import ApiPublisher
import main
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from gsm.services import create_reader
from sqlalchemy.pool import StaticPool


class IocContainer(containers.DeclarativeContainer):

    config = providers.Configuration('config')
    logger = providers.Singleton(logging.Logger, name='NYSS-Gateway')

    database_engine = providers.Singleton(
        create_engine,
        config.database.url,
        connect_args={'check_same_thread': False},
        # poolclass=StaticPool,
    )

    session_maker = providers.Singleton(
        sessionmaker,
        bind=database_engine
    )

    session_factory = providers.Singleton(
        scoped_session,
        session_maker
    )

    sms_service = providers.Factory(
        SmsService,
        logger=logger,
        sessionFactory=session_factory
    )

    sms_reader = providers.Singleton(
        create_reader,
        reader_type=config.gsm.handler,
        smsService=sms_service,
        logger=logger
    )

    api_publisher = providers.Factory(
        ApiPublisher,
        API_URL=config.api.url,
        API_ID=config.api.id,
        API_KEY=config.api.key,
        logger=logger,
        smsService=sms_service,
    )

    createDatabase = providers.Callable(
        main.createDatabase, engine=database_engine)

    main = providers.Callable(
        main.main,
        save_service=sms_service,
    )
