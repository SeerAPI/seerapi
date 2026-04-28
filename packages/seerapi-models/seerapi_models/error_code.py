from sqlmodel import Field

from seerapi_models.build_model import BaseResModel, ConvertToORM


class BaseErrorCode(BaseResModel):
    name: str = Field(description='名称')
    message: str = Field(description='错误消息')

    @classmethod
    def resource_name(cls) -> str:
        return 'error_code'


class ErrorCode(BaseErrorCode, ConvertToORM['ErrorCodeORM']):
    @classmethod
    def get_orm_model(cls) -> 'type[ErrorCodeORM]':
        return ErrorCodeORM

    def to_orm(self) -> 'ErrorCodeORM':
        return ErrorCodeORM(
            id=self.id,
            name=self.name,
            message=self.message,
        )


class ErrorCodeORM(BaseErrorCode, table=True):
    pass
