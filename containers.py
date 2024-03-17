from dependency_injector import containers, providers

from services.user_service import UserService
from services.user_states_service import UserStatesService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_service = providers.Singleton(
        UserService
    )

    user_states_service = providers.Singleton(
        UserStatesService
    )


