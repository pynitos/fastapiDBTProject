from diary_ms.application.medicament.dto.medicament import OwnMedicamentDTO
from diary_ms.application.medicament.exceptions.medicament import MedicamentIdNotProvidedError
from diary_ms.domain.model.entities.medicament import Medicament


class MedicamentDTOMapper:
    @staticmethod
    def dm_to_dto(dm: Medicament) -> OwnMedicamentDTO:
        if not dm.id.value:
            raise MedicamentIdNotProvidedError
        return OwnMedicamentDTO(
            id=dm.id.value,
            user_id=dm.user_id.value,
            name=dm.name.value,
            dosage=dm.dosage.value,
        )

    @classmethod
    def dm_list_to_dto_list(cls, dm_list: list[Medicament]) -> list[OwnMedicamentDTO]:
        return [cls.dm_to_dto(dm) for dm in dm_list]
