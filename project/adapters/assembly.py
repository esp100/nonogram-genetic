from dependency_injector import containers, providers
from project.domain.nonogram_service import NonogramServiceImpl

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["project.blueprints"])
    nonogram_service = providers.Factory(NonogramServiceImpl)