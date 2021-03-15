# Increments for odds range filter
incs = list()
incs.append({'min': 1.00, 'max': 2.00, 'value': 0.01, 'round': 2})
incs.append({'min': 2.00, 'max': 3.00, 'value': 0.02, 'round': 2})
incs.append({'min': 3.00, 'max': 5.00, 'value': 0.05, 'round': 2})
incs.append({'min': 5.00, 'max': 10.00, 'value': 0.1, 'round': 1})
incs.append({'min': 10.00, 'max': 20.00, 'value': 0.2, 'round': 1})
incs.append({'min': 20.00, 'max': 30.00, 'value': 0.5, 'round': 1})
incs.append({'min': 30.00, 'max': 50.00, 'value': 1, 'round': 0})
incs.append({'min': 50.00, 'max': 100.00, 'value': 2, 'round': 0})
incs.append({'min': 100.00, 'max': 500.00, 'value': 5, 'round': 0})
incs.append({'min': 500.00, 'max': 1000.00, 'value': 10, 'round': 0})

ODDS_incs = list()
x = 1
while x < 1000:
    for increment in incs:
        if increment['max'] > x >= increment['min']:
            if increment['round'] == 0:
                x = int(x)
            ODDS_incs.append(round(x + increment['value'], increment['round']))
            x += round(increment['value'], increment['round'])
            break
