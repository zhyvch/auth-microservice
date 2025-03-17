from dataclasses import dataclass

from infrastrusture.brokers.base import BaseMessageBroker


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    ...
