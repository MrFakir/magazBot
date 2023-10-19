# Информация о расчёте зп недоступна, коммерческая тайна
def dry_pay(cash, card):
    message_cash = ''
    message_card = ''
    if cash and cash > 0:
        message_cash = ''
        if cash > 100000:
            message_cash = 'Кажется кто-то ошибся с нулями, в наличных.'
            cash = 0
        cash = cash * 0
    else:
        cash = 0

    if card and card > 0:
        if card > 100000:
            message_card = 'Кажется кто-то ошибся с нулями в безнале.'
            card = 0
        card = card * 0
    else:
        card = 0

    if message_card or message_cash:
        message = message_card + '\n' + message_cash
        return cash + card, message
    else:
        return cash + card, ''


def final_zp_tax(zp):
    zp = zp - (zp * 0.13)
    return str(f'{zp:.2f}')


def main():
    dp, text = dry_pay(0, 0)
    print(final_zp_tax(dp))
    print(text)


if __name__ == '__main__':
    main()
