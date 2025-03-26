from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'example@mail.com',
                'password': 'Very$ecurePa$$w0rd1234',
            },
        }


class TokenPairSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        json_schema_extra = {
            'example': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.'
                                'SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkphbmUgRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.'
                                 'cMErWtEf7DxCXJl8C9q0L7ttkm-Ex54UWHsOCMGbtUc',
            },
        }



class RefreshTokenSchema(BaseModel):
    refresh_token: str

    class Config:
        json_schema_extra = {
            'example': {
                'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'
                                 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkphbmUgRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.'
                                 'cMErWtEf7DxCXJl8C9q0L7ttkm-Ex54UWHsOCMGbtUc',
            },
        }


class UpdateUserCredentialsSchema(BaseModel):
    email: str | None = None
    password: str | None = None

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'example@mail.com',
                'password': 'Very$ecurePa$$w0rd1234',
            }
        }
