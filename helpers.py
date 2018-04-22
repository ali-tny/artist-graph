def build_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine('sqlite:///pitchfork_example.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session