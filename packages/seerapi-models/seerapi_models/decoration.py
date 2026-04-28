from sqlmodel import Field

from seerapi_models.build_model import BaseResModel, ConvertToORM


class BaseDecoration(BaseResModel):
    name: str = Field(description='资源名称')
    desc: str = Field(description='资源描述')
    icon_id: int = Field(
        description='资源ID（对应profilephoto配置中的icon字段）', primary_key=True
    )


class AvatarHead(BaseDecoration, ConvertToORM['AvatarHeadORM']):
    @classmethod
    def resource_name(cls) -> str:
        return 'avatar_head'

    @classmethod
    def get_orm_model(cls) -> type['AvatarHeadORM']:
        return AvatarHeadORM

    def to_orm(self) -> 'AvatarHeadORM':
        return AvatarHeadORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            icon_id=self.icon_id,
        )


class AvatarHeadORM(AvatarHead, table=True):
    pass


class AvatarFrame(BaseDecoration, ConvertToORM['AvatarFrameORM']):
    @classmethod
    def resource_name(cls) -> str:
        return 'avatar_frame'

    @classmethod
    def get_orm_model(cls) -> type['AvatarFrameORM']:
        return AvatarFrameORM

    def to_orm(self) -> 'AvatarFrameORM':
        return AvatarFrameORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            icon_id=self.icon_id,
        )


class AvatarFrameORM(AvatarFrame, table=True):
    pass


class NamecardBackground(BaseDecoration, ConvertToORM['NamecardBackgroundORM']):
    @classmethod
    def resource_name(cls) -> str:
        return 'namecard_background'

    @classmethod
    def get_orm_model(cls) -> type['NamecardBackgroundORM']:
        return NamecardBackgroundORM

    def to_orm(self) -> 'NamecardBackgroundORM':
        return NamecardBackgroundORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            icon_id=self.icon_id,
        )


class NamecardBackgroundORM(NamecardBackground, table=True):
    pass


class NicknameBackground(BaseDecoration, ConvertToORM['NicknameBackgroundORM']):
    @classmethod
    def resource_name(cls) -> str:
        return 'nickname_background'

    @classmethod
    def get_orm_model(cls) -> type['NicknameBackgroundORM']:
        return NicknameBackgroundORM

    def to_orm(self) -> 'NicknameBackgroundORM':
        return NicknameBackgroundORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            icon_id=self.icon_id,
        )


class NicknameBackgroundORM(NicknameBackground, table=True):
    pass


class HomepageBackground(BaseDecoration, ConvertToORM['HomepageBackgroundORM']):
    @classmethod
    def resource_name(cls) -> str:
        return 'homepage_background'

    @classmethod
    def get_orm_model(cls) -> type['HomepageBackgroundORM']:
        return HomepageBackgroundORM

    def to_orm(self) -> 'HomepageBackgroundORM':
        return HomepageBackgroundORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            icon_id=self.icon_id,
        )


class HomepageBackgroundORM(HomepageBackground, table=True):
    pass


class Emoji(BaseDecoration, ConvertToORM['EmojiORM']):
    @classmethod
    def resource_name(cls) -> str:
        return 'emoji'

    @classmethod
    def get_orm_model(cls) -> type['EmojiORM']:
        return EmojiORM

    def to_orm(self) -> 'EmojiORM':
        return EmojiORM(
            id=self.id,
            name=self.name,
            desc=self.desc,
            icon_id=self.icon_id,
        )


class EmojiORM(Emoji, table=True):
    pass
