def message_start(user):
    """Message of /start command"""
    message = f"Hi, {user.first_name}!\n"
    message += 'To see your portfolios /portfolios\n'
    return message


def message_portfolios(user, portfolios):
    """Message of /portfolios command"""
    message = ''
    if len(portfolios) > 0:
        message += 'Your portfolios:\n'
        for row in portfolios:
            message += f'{row} {row.command()}\n'
    else:
        message += 'You have no portfolios\n'
    message += 'Create new /newportfolio\n'
    return message

