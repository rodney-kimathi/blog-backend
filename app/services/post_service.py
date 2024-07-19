from sqlmodel import select, Session

from app.models.post_models import Post, PostRequest


def create_post(user_id: int, post_request: PostRequest, session: Session) -> Post:
    post = Post(user_id=user_id, **post_request.model_dump())

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


def read_posts(user_id: int, session: Session) -> list[Post]:
    query = select(Post).where(Post.user_id == user_id)

    return session.exec(query).all()


def read_post(user_id: int, post_id: int, session: Session) -> Post:
    post = session.get(Post, post_id)

    if not post or post.user_id != user_id:
        raise ValueError("Post not found")

    return post
