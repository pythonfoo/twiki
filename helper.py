import config
import logging

log = logging.getLogger(__name__)


def any_dry_run():
    dry_run_count = 0

    if config.TWITTER_ACTIVE and config.TWITTER_DRY_RUN:
        dry_run_count += 1

    if config.MATRIX_ACTIVE and config.MATRIX_DRY_RUN:
        dry_run_count += 1

    if config.MASTODON_ACTIVE and config.MASTODON_DRY_RUN:
        dry_run_count += 1

    if config.DISCORD_ACTIVE and config.DISCORD_DRY_RUN:
        dry_run_count += 1

    return dry_run_count > 0


def data_valid(data_list):
    for config_data in data_list:
        if config_data == '':
            return False

    return True


def can_twitter():
    required_config_data = [
        config.TWITTER_TOKEN,
        config.TWITTER_TOKEN_SECRET,
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET,
    ]

    return data_valid(required_config_data)


def can_mastodon():
    required_config_data = [
        config.MASTODON_API_BASE_URL,
        config.MASTODON_ACCESS_TOKEN
    ]

    return data_valid(required_config_data)


def can_matrix():
    required_config_data = [
        config.MATRIX_SERVER,
        config.MATRIX_USER_NAME,
        config.MATRIX_PASSWORD,
        config.MATRIX_ROOM_ID
    ]

    return data_valid(required_config_data)


def can_discord():
    required_config_data = [
        config.DISCORD_APP_ID,
        config.DISCORD_TOKEN,
        config.DISCORD_CHANNEL_ID,
    ]

    return data_valid(required_config_data)
