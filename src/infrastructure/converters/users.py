from domain.entities.users import UserCredentialsEntity
from domain.value_objects.users import EmailVO, str
from infrastructure.models.users import UserCredentialsModel


def convert_user_entity_to_model(user_creds: UserCredentialsEntity) -> UserCredentialsModel:
    return UserCredentialsModel(
        id=user_creds.id,
        email=user_creds.email.as_generic(),
        created_at=user_creds.created_at,
        user_id=user_creds.user_id,
        hashed_password=user_creds.hashed_password,
    )

def convert_user_model_to_entity(user_creds: UserCredentialsModel) -> UserCredentialsEntity:
    return UserCredentialsEntity(
        id=user_creds.id,
        created_at=user_creds.created_at,
        email=EmailVO(user_creds.email),
        user_id=user_creds.user_id,
        hashed_password=user_creds.hashed_password,
    )