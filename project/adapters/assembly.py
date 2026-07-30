from dependency_injector import containers, providers
from project.domain.nonogram_service import NonogramServiceImpl
from project.adapters.csv_adapter import CSVAdapter

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["project.blueprints"])
    csv_adapter = providers.Factory(
        CSVAdapter,
    )

    nonogram_service = providers.Factory(
        NonogramServiceImpl,
        csv_adapter=csv_adapter,
    )