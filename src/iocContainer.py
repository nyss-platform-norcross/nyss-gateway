from dependency_injector import containers, providers

import logging
import sqlite3
from smshandling.smsPersistentService import SmsPersistentService
from smshandling.smsPublisherService import SmsPublisherService
from publishing.services import ApiPublisher
import main
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from gsm.services import DummySMSReader
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

    api_publisher = providers.Factory(
        ApiPublisher,
        API_URL=config.api.url,
        API_ID=config.api.id,
        API_KEY=config.api.key,
        logger=logger,
    )

    save_service = providers.Factory(
        SmsPersistentService,
        logger=logger,
        sessionFactory=session_factory
    )

    sms_reader = providers.Singleton(
        DummySMSReader,
        smsHandler=save_service
    )

    if config.gsm.handler == 'HUAWEI':
        sms_reader = providers.Singleton(
            DummySMSReader,
            smsHandler=save_service
        )
    elif config.gsm.handler == 'DUMMY':
        sms_reader = providers.Singleton(
            DummySMSReader,
            smsHandler=save_service
        )

    sms_publisher = providers.Singleton(
        SmsPublisherService,
        logger=logger,
        smsPersistentService=save_service,
        publisher=api_publisher)

    createDatabase = providers.Callable(
        main.createDatabase, engine=database_engine)

    main = providers.Callable(
        main.main,
        save_service=save_service,
        publisher=sms_publisher,
    )
