from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.validators import SenhaMinima


class LoginRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "gabriel@example.com",
                    "senha": "senha1234",
                }
            ]
        }
    )

    email: EmailStr
    senha: SenhaMinima


class TokenResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                }
            ]
        }
    )

    access_token: str
    token_type: str = Field(default="bearer")
