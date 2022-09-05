import os
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    DateTime,
    Enum,
    Integer,
    ForeignKey,
    func,
    String,
    Table,
    Time,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


def _psql_uri():
    username = os.environ.get("PGUSER")
    password = os.environ.get("PGPASSWORD")
    if username and password:
        return (
            f"postgresql+psycopg2://{username}:{password}@/"
            f'{os.environ.get("PGDATABASE")}'
            f'?host={os.environ.get("PGHOST")}'
        )
    else:
        return (
            f'postgresql+psycopg2://{os.environ.get("PGHOST")}:5432/'
            f'{os.environ.get("PGDATABASE")}'
        )


engine = create_engine(_psql_uri())
Session = sessionmaker(engine)
Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    email = Column(String(320), primary_key=True)
    uuid = Column(
        String(36),
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    active = Column(Boolean, default=True, nullable=False)
    last_email = Column(DateTime)
    signup_time = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Account {self.email}>"


class Subreddit(Base):
    __tablename__ = "subreddit"

    name = Column(String(21), primary_key=True)

    def __repr__(self):
        return f"<Subreddit {self.name}>"


class SubredditPost(Base):
    __tablename__ = "subreddit_post"

    id = Column(String(128), primary_key=True)
    subreddit_name = Column(
        String(21),
        ForeignKey("subreddit.name", onupdate="cascade"),
        nullable=False,
    )
    subreddit = relationship("Subreddit")
    title = Column(String(300), nullable=False)
    url = Column(String(2000), nullable=False)

    scraped_at = Column(DateTime, server_default=func.now(), nullable=False)
    preview_image_url = Column(String(2000))
    permalink_url = Column(String(2000))
    num_comments = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<SubredditPost {self.id}>"


email_event_subreddit = Table(
    "email_event_subreddit",
    Base.metadata,
    Column(
        "email_event_id",
        Integer,
        ForeignKey("email_event.id", ondelete="cascade"),
        primary_key=True,
    ),
    Column(
        "subreddit_name",
        String(21),
        ForeignKey("subreddit.name", onupdate="cascade"),
        primary_key=True,
    ),
)


class EmailEvent(Base):
    """
    Recurring event model for emails to be sent to accounts.
    """

    __tablename__ = "email_event"

    id = Column(Integer, primary_key=True)
    account_email = Column(
        String(320),
        ForeignKey("account.email", onupdate="cascade"),
        nullable=False,
    )
    account = relationship("Account", backref="email_events")
    time_of_day = Column(Time, nullable=False)
    day_of_week = Column(Integer)

    subreddits = relationship(
        "Subreddit",
        backref="email_events",
        order_by="Subreddit.name",
        secondary=email_event_subreddit,
    )


class ScrapeRecordSubredditPost(Base):
    """
    The relationship between scrape_records and subreddit_posts
    """

    __tablename__ = "scrape_record_subreddit_post"

    scrape_record_id = Column(Integer, ForeignKey("scrape_record.id"), primary_key=True)
    subreddit_post_id = Column(
        String(128), ForeignKey("subreddit_post.id"), primary_key=True
    )
    ordinal = Column(Integer, nullable=False)

    scrape_record = relationship("ScrapeRecord")
    subreddit_post = relationship("SubredditPost")


class ScrapeRecord(Base):
    """
    A grouping of subreddit posts from a scraping event
    """

    __tablename__ = "scrape_record"

    id = Column(Integer, primary_key=True)
    interval = Column(Enum("daily", "weekly", name="interval_enum"), nullable=False)
    scrape_time = Column(DateTime, server_default=func.now(), nullable=False)
    subreddit_name = Column(
        String(21), ForeignKey("subreddit.name", onupdate="cascade")
    )

    subreddit = relationship("Subreddit")
    scrape_record_subreddit_posts = relationship("ScrapeRecordSubredditPost")
    subreddit_posts = relationship(
        "SubredditPost",
        backref="scrape_records",
        order_by="ScrapeRecordSubredditPost.ordinal",
        secondary=ScrapeRecordSubredditPost.__table__,
    )
