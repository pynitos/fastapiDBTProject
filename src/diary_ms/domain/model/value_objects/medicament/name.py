from dataclasses import dataclass

from src.diary_ms.domain.common.exceptions.base import DomainValueError
from src.diary_ms.domain.common.model.value_objects.base import ValueObject

MAX_MED_NAME_VALUE = 20
MIN_MED_NAME_VALUE = 3


class WrongMedicamentNameValueError(ValueError, DomainValueError):
    pass


@dataclass(frozen=True)
class MedicamentName(ValueObject[str]):
    def _validate(self) -> None:
        """Validate medicament name length and content"""
        value = self.value
        # Check for empty value
        if not value or not isinstance(value, str):
            raise WrongMedicamentNameValueError(
                f"Medicament name cannot be empty. Got: {value}"
            )

        # Strip whitespace for validation
        stripped_value = value.strip()

        # Check length after stripping
        name_length = len(stripped_value)

        if name_length < MIN_MED_NAME_VALUE:
            raise WrongMedicamentNameValueError(
                f"Medicament name must be at least {MIN_MED_NAME_VALUE} characters long. "
                f"Current length: {name_length}"
            )

        if name_length > MAX_MED_NAME_VALUE:
            raise WrongMedicamentNameValueError(
                f"Medicament name must not exceed {MAX_MED_NAME_VALUE} characters. "
                f"Current length: {name_length}"
            )

        # Optional: Check for valid characters (letters, numbers, spaces, hyphens)
        import re
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', stripped_value):
            raise WrongMedicamentNameValueError(
                f"Medicament name contains invalid characters. "
                f"Use only letters, numbers, spaces and hyphens. Got: {stripped_value}"
            )
        # Check if name consists only of whitespace
        if stripped_value.isspace():
            raise WrongMedicamentNameValueError(
                "Medicament name cannot consist only of whitespace characters"
            )
