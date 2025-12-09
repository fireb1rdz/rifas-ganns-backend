from abc import ABC, abstractmethod

class BaseGateway(ABC):
    @abstractmethod
    def create_customer(self, data: dict) -> str:
        """Creates an user and returns it's ID in the gateway database

        Args:
            user (dict): Dict containing user info

        Returns:
            dict: User's ID
        """
        pass

