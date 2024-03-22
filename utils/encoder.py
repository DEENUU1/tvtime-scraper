import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    """
    JSON encoder class to handle UUID objects.
    """

    def default(self, obj):
        """
        Override default method to handle UUID objects.

        Args:
            obj: Object to encode.

        Returns:
            str: Encoded UUID string if obj is UUID, otherwise default encoding.
        """
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)
