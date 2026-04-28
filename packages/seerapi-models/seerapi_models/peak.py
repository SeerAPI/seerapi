from datetime import datetime

from sqlmodel import Field

from seerapi_models.build_model import BaseResModel, ConvertToORM


class BasePeakSeason(BaseResModel):
    id: int = Field(description='该赛季的ID，固定为1', primary_key=True)
    start_time: datetime = Field(description='该赛季的开始时间')
    end_time: datetime = Field(
        description='该赛季的结束时间，由 `start_time`'
        '加上固定时长计算得出，游戏内没有准确数据'
    )

    @classmethod
    def resource_name(cls) -> str:
        return 'peak_season'


class PeakSeason(BasePeakSeason, ConvertToORM['PeakSeasonORM']):
    @classmethod
    def get_orm_model(cls) -> 'type[PeakSeasonORM]':
        return PeakSeasonORM

    def to_orm(self) -> 'PeakSeasonORM':
        return PeakSeasonORM(
            id=self.id,
            start_time=self.start_time,
            end_time=self.end_time,
        )


class PeakSeasonORM(BasePeakSeason, table=True):
    pass
