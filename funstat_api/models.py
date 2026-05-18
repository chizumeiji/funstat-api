from pydantic import BaseModel, Field


class TechInfo(BaseModel):
    request_cost: float
    current_ballance: float
    request_duration: str


class Paging(BaseModel):
    total: int
    current_page: int = Field(alias="currentPage")
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    model_config = {"populate_by_name": True}


class ResolvedUser(BaseModel):
    id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool
    is_bot: bool
    has_premium: bool | None = None


class ChatInfo(BaseModel):
    id: int
    title: str
    is_private: bool = Field(alias="isPrivate")
    username: str | None = None
    model_config = {"populate_by_name": True}


class ChatInfoExt(BaseModel):
    id: int
    title: str
    is_private: bool = Field(alias="isPrivate")
    is_channel: bool = Field(alias="isChannel")
    username: str | None = None
    link: str | None = None
    model_config = {"populate_by_name": True}


class UserStatsMin(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool
    is_active: bool
    first_msg_date: str | None = None
    last_msg_date: str | None = None
    total_msg_count: int
    msg_in_groups_count: int
    adm_in_groups: int
    usernames_count: int
    names_count: int
    total_groups: int


class UserStats(UserStatsMin):
    is_cyrillic_primary: bool | None = None
    lang_code: str | None = None
    unique_percent: float | None = None
    circle_count: int
    voice_count: int
    reply_percent: float
    media_percent: float
    link_percent: float
    favorite_chat: ChatInfo | None = None
    media_usage: str | None = None
    stars_val: int | None = None
    personal_channel_id: int | None = None
    gift_count: int | None = None
    stars_level: int | None = None
    birth_day: int | None = None
    birth_month: int | None = None
    birth_year: int | None = None
    about: str | None = None


class UserMsg(BaseModel):
    date: str
    message_id: int = Field(alias="messageId")
    reply_to_message_id: int | None = Field(default=None, alias="replyToMessageId")
    media_code: int | None = Field(default=None, alias="mediaCode")
    media_name: str | None = Field(default=None, alias="mediaName")
    text: str | None = None
    group: ChatInfo
    model_config = {"populate_by_name": True}


class UserNameInfo(BaseModel):
    name: str
    date_time: str


class UsrChatInfo(BaseModel):
    chat: ChatInfo
    last_message_id: int = Field(alias="lastMessageId")
    messages_count: int = Field(alias="messagesCount")
    last_message: str | None = Field(default=None, alias="lastMessage")
    first_message: str | None = Field(default=None, alias="firstMessage")
    is_admin: bool = Field(alias="isAdmin")
    is_left: bool = Field(alias="isLeft")
    model_config = {"populate_by_name": True}


class GroupMember(BaseModel):
    id: int
    username: str | None = None
    name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_admin: bool | None = None
    is_active: bool
    today_msg: int
    has_prem: bool | None = None
    has_photo: bool
    dc_id: int | None = None


class GiftRelationInfo(BaseModel):
    last_gift_date: str | None = None
    from_user_id: int
    from_first_name: str | None = None
    from_last_name: str | None = None
    from_main_username: str | None = Field(default=None, alias="from_mainUsername")
    from_is_active: bool
    to_user_id: int
    to_first_name: str | None = None
    to_last_name: str | None = None
    to_main_username: str | None = Field(default=None, alias="to_mainUsername")
    to_is_active: bool
    model_config = {"populate_by_name": True}


class StickerInfo(BaseModel):
    sticker_set_id: int
    last_seen: str
    min_seen: str
    resolved: str | None = None
    title: str | None = None
    short_name: str | None = None
    stickers_count: int | None = None


class UCommonGroupInfo(BaseModel):
    user_id: int
    common_groups: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    is_user_active: bool


class UsernameUsageModel(BaseModel):
    actual_users: list[ResolvedUser] | None = Field(default=None, alias="actualUsers")
    usage_by_users_in_the_past: list[ResolvedUser] | None = Field(default=None, alias="usageByUsersInThePast")
    actual_groups_or_channels: list[ChatInfoExt] | None = Field(default=None, alias="actualGroupsOrChannels")
    mention_by_channel_or_group_desc: list[ChatInfoExt] | None = Field(
        default=None, alias="mentionByChannelOrGroupDesc"
    )
    model_config = {"populate_by_name": True}


class WhoWroteText(BaseModel):
    message_id: int
    user_id: int
    date: str
    name: str | None = None
    username: str | None = None
    is_active: bool
    group: ChatInfoExt
    text: str | None = None


class PingResult(BaseModel):
    request_ping: str
    responce_ping: float


class UserResult(BaseModel):
    id: int
    user_name: str | None = Field(default=None, alias="userName")
    first_name: str
    last_name: str | None = None
    name: str | None = None
    is_bot: bool
    model_config = {"populate_by_name": True}


class UserResultPagedNoCount(BaseModel):
    total: int
    data: list[UserResult]
    is_last_page: bool | None = Field(default=None, alias="isLastPage")
    page_size: int | None = Field(default=None, alias="pageSize")
    current_page: int | None = Field(default=None, alias="currentPage")
    total_pages: int | None = Field(default=None, alias="totalPages")
    is_sliding: bool | None = Field(default=None, alias="isSliding")
    model_config = {"populate_by_name": True}


class NameUsageResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: UserResultPagedNoCount | None = None


# Base API Response Wrappers
class ResolvedUserResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[ResolvedUser] | None = None


class UserStatsMinResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: UserStatsMin | None = None


class UserStatsResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: UserStats | None = None


class UserMsgPagedResponse(BaseModel):
    success: bool
    tech: TechInfo
    paging: Paging
    data: list[UserMsg] | None = None


class UserNameInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[UserNameInfo] | None = None


class UsrChatInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[UsrChatInfo] | None = None


class GroupMemberResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[GroupMember] | None = None


class GiftRelationResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[GiftRelationInfo] | None = None


class StickerInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[StickerInfo] | None = None


class UCommonGroupInfoResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[UCommonGroupInfo] | None = None


class UsernameUsageResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: UsernameUsageModel | None = None


class ChatInfoExtResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: list[ChatInfoExt] | None = None


class WhoWroteTextPaged(BaseModel):
    total: int
    data: list[WhoWroteText]
    is_last_page: bool | None = Field(default=None, alias="isLastPage")
    page_size: int | None = Field(default=None, alias="pageSize")
    current_page: int | None = Field(default=None, alias="currentPage")
    total_pages: int | None = Field(default=None, alias="totalPages")
    is_sliding: bool | None = Field(default=None, alias="isSliding")
    model_config = {"populate_by_name": True}


class WhoWroteTextResponse(BaseModel):
    success: bool
    tech: TechInfo
    data: WhoWroteTextPaged | None = None


# New models for previously untyped endpoints
class ReputationResponse(BaseModel):
    user_id: int
    num_votes: int
    reputation_code: str | None = None
    bayesian_average: float | None = None
    simple_average: float | None = None
    positive_count: int | None = None
    negative_count: int | None = None
    first_time: str | None = None
    last_time: str | None = None
    anon_votes_count: int | None = None
    review_count: int | None = None
    reputation_name: str | None = None


class GroupInfo(BaseModel):
    id: int
    title: str
    is_private: bool = Field(alias="isPrivate")
    is_channel: bool = Field(alias="isChannel")
    username: str | None = None
    link: str | None = None
    members_count: int | None = Field(default=None, alias="membersCount")
    has_photo: bool | None = Field(default=None, alias="hasPhoto")
    about: str | None = None
    is_scam: bool | None = Field(default=None, alias="isScam")
    is_fake: bool | None = Field(default=None, alias="isFake")
    model_config = {"populate_by_name": True}


class TodayGroupStat(BaseModel):
    rank: int | None = None
    active_users_count: int | None = Field(default=None, alias="activeUsersCount")
    messages_count: int | None = Field(default=None, alias="messagesCount")
    text_msg_count: int | None = Field(default=None, alias="textMsgCount")
    media_msg_count: int | None = Field(default=None, alias="mediaMsgCount")
    voice_count: int | None = Field(default=None, alias="voiceCount")
    circle_count: int | None = Field(default=None, alias="circleCount")
    non_cyrillic_rate: float | None = Field(default=None, alias="nonCyrillicRate")
    avg_unique_percent: float | None = Field(default=None, alias="avgUniquePercent")
    avg_media_percent: float | None = Field(default=None, alias="avgMediaPercent")
    avg_link_percent: float | None = Field(default=None, alias="avgLinkPercent")
    model_config = {"populate_by_name": True}


class GroupInfoResponse(BaseModel):
    info: GroupInfo
    today_group_stat: TodayGroupStat | None = None
