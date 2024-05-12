import logging

logger = logging.getLogger(__name__)


def log_post_walking_create(post):
    """Записывает лог создания записи в журнале обходов."""
    logger.info(
        f'PostWalking (id: {post.id}) was created. '
        f'User: {(post.author.username).upper()}'
    )


def log_post_walking_edit(post):
    """Записывает лог изменения записи в журнале обходов."""
    logger.info(
        f'PostWalking (id: {post.id}) was edited. '
        f'User: {(post.author.username).upper()}'
    )


def log_resolution_create(resolution):
    """Записывает лог создания резолюции."""
    logger.info(
        f'Resolution (id: {resolution.id}) was added. '
        f'Text: {resolution.text}. '
        f'User: {(resolution.author.username).upper()}'
    )


def log_resolution_edit(resolution, username):
    """Записывает лог изменения резолюции."""
    logger.info(
        f'Resolution (id: {resolution.id}) was changed. '
        f'New text: {resolution.text}. '
        f'User: {username.upper()}'
    )


def log_post_repair_work_create(post):
    """Записывает лог создания записи в журнале ремонтных работ."""
    logger.info(
        f'PostRepairWork (id: {post.id}) was created. '
        f'User: {(post.author.username).upper()}'
    )


def log_post_repair_work_edit(post):
    """Записывает лог изменения записи в журнале ремонтных работ."""
    logger.info(
        f'PostRepairWork (id: {post.id}) was edited. '
        f'User: {(post.author.username).upper()}'
    )


def log_post_order_create(post):
    """Записывает лог создания записи в журнале учета работ."""
    logger.info(
        f'PostOrder (id: {post.id}) was created. '
        f'User: {(post.author.username).upper()}'
    )


def log_post_order_edit(post):
    """Записывает лог изменения записи в журнале учета работ."""
    logger.info(
        f'PostOrder (id: {post.id}) was edited. '
        f'User: {(post.author.username).upper()}'
    )
