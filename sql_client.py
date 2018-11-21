from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER, BOOLEAN, TIMESTAMP, BIGINT, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine, Connection


PUBLIC_SCHEMA = {"schema": "public"}

Base = declarative_base()


class SQLClient:  # todo: rename to psql client
    engine = None
    connection = None
    session = None

    def __enter__(self):
        operations_connection_string = get_db_connection_string()
        SQLClient.engine: Engine = create_engine(operations_connection_string)
        SQLClient.connection: Connection = SQLClient.engine.connect()
        session_maker = sessionmaker(expire_on_commit=False)
        SQLClient.session = session_maker(bind=SQLClient.engine)

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if not exception_type:
            SQLClient.session.commit()

            SQLClient.session.close()
            SQLClient.connection.close()
            SQLClient.engine.dispose()


def get_db_connection_string():
    user_name = ""
    password = ""
    host_name = ""
    db_name = ""
    operations_connection_string = f"postgresql://{user_name}:{password}@{host_name}:5432/{db_name}"
    return operations_connection_string


class KnessetMember(Base):
    __tablename__ = "twitter_knesset_members"
    __table_args__ = PUBLIC_SCHEMA

    faction = Column("faction", TEXT)
    hebrew_name = Column("hebrew_name", TEXT)
    twitter_screen_name = Column("twitter_screen_name", TEXT)

    knesset_member_id = Column("knesset_member_id", INTEGER, primary_key=True)
    created_in_db = Column("created_in_db", TIMESTAMP)


class TwitterUserProfile(Base):
    __tablename__ = "twitter_knesset_user_profiles"
    __table_args__ = PUBLIC_SCHEMA

    twitter_user_id = Column("twitter_user_id", BIGINT)
    name = Column("name", TEXT)
    screen_name = Column("screen_name", TEXT)
    description = Column("description", TEXT)
    created_at = Column("created_at", TIMESTAMP)
    geo_enabled = Column("geo_enabled", BOOLEAN)
    lang = Column("lang", TEXT)
    url = Column("url", TEXT)
    verified = Column("verified", BOOLEAN)
    protected = Column("protected", BOOLEAN)

    faction = Column("faction", TEXT)
    knesset_id = Column("knesset_id", INTEGER)
    is_active = Column("is_active", BOOLEAN)

    favourites_count = Column("favourites_count", INTEGER)
    followers_count = Column("followers_count", INTEGER)
    friends_count = Column("friends_count", INTEGER)
    listed_count = Column("listed_count", INTEGER)
    statuses_count = Column("statuses_count", INTEGER)

    # TODO: remove deprecated
    contributors_enabled = Column("contributors_enabled", BOOLEAN)
    default_profile = Column("default_profile", BOOLEAN)
    default_profile_image = Column("default_profile_image", BOOLEAN)
    has_extended_profile = Column("has_extended_profile", BOOLEAN)
    is_translation_enabled = Column("is_translation_enabled", BOOLEAN)
    is_translator = Column("is_translator", BOOLEAN)
    translator_type = Column("translator_type", TEXT)

    profile_background_tile = Column("profile_background_tile", BOOLEAN)
    profile_use_background_image = Column("profile_use_background_image", BOOLEAN)
    profile_background_image_url = Column("profile_background_image_url", TEXT)
    profile_background_image_url_https = Column("profile_background_image_url_https", TEXT)
    profile_banner_url = Column("profile_banner_url", TEXT)
    profile_image_url = Column("profile_image_url", TEXT)
    profile_image_url_https = Column("profile_image_url_https", TEXT)
    profile_background_color = Column("profile_background_color", TEXT)
    profile_link_color = Column("profile_link_color", TEXT)
    profile_sidebar_border_color = Column("profile_sidebar_border_color", TEXT)
    profile_sidebar_fill_color = Column("profile_sidebar_fill_color", TEXT)
    profile_sidebar_text_color = Column("profile_sidebar_text_color", TEXT)

    knesset_user_profile_id = Column("knesset_user_profile_id", INTEGER, primary_key=True)
    created_in_db = Column("created_in_db", TIMESTAMP)


class Tweet(Base):
    __tablename__ = "twitter_knesset_tweets"
    __table_args__ = PUBLIC_SCHEMA

    tweet_id = Column("tweet_id", BIGINT, primary_key=True)
    created_at = Column("created_at", TIMESTAMP)
    text = Column("text", TEXT)
    source = Column("source", TEXT)
    truncated = Column("truncated", BOOLEAN)
    reply_to_tweet_id = Column("reply_to_tweet_id", BIGINT)
    reply_to_user_id = Column("reply_to_user_id", BIGINT)
    reply_to_user_name = Column("reply_to_user_name", TEXT)
    user = Column("user", JSON)
    coordinates = Column("coordinates", JSON)
    place = Column("place", JSON)
    is_quote = Column("is_quote", BOOLEAN)
    quote_of_tweet_id = Column("quote_of_tweet_id", BIGINT)
    quoted_tweet = Column("quoted_tweet", JSON)
    retweeted_tweet = Column("retweeted_tweet", JSON)
    entities = Column("entities", JSON)
    extended_entities = Column("extended_entities", JSON)
    possibly_sensitive = Column("possibly_sensitive", BOOLEAN)
    filter_level = Column("filter_level", TEXT)
    lang = Column("lang", TEXT)
    matching_rules = Column("matching_rules", ARRAY(JSON))
    withheld_in_countries = Column("withheld_in_countries", ARRAY(TEXT))
    created_in_db = Column("created_in_db", TIMESTAMP)
