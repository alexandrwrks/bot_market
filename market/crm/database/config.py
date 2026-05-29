from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(url="sqlite+aiosqlite:///crm_sys.db", echo=False)

new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
