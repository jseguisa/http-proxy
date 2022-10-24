#!/usr/bin/env python3

cache_duration = 10

json_filter_enable = True

json_account_data_filters = [
    '/data/account/CmeSmpId',
    '/data/account/DailyLoss',
    '/data/account/DailyLossPercent',
    '/data/account/EquitiesMarketValue',
    '/data/account/EquitiesPurchase',
    '/data/account/EquitiesPurchaseSale',
    '/data/account/EquitiesSale',
    '/data/account/EquityHaircutPercent',
    '/data/account/FilledFuturesOpenTradeEquity',
    '/data/account/MarginCredit',
    '/data/account/NominalInitialMarginRequirementPositionsOnly',
    '/data/account/NominalMaintenanceMarginRequirementPositionsOnly',
    '/data/account/PotentialBuyOptionPremium',
    '/data/account/PotentialEquityPurchase',
    '/data/account/PotentialNetOptionValue',
    '/data/account/SmpInst',
    '/data/account/StartOfDayInitialMarginRequirementPositionsOnly',
    '/data/account/StartOfDayMaintenanceMarginRequirementPositionsOnly',
    '/data/account/StocksPurchase',
    '/data/account/StocksPurchaseSale',
    '/data/account/StocksSale',
    '/data/account/groups',
    '/data/account/isDiscretionary',
    '/data/account/isHedge',
    '/data/account/isInHouse',
    '/data/account/isOmnibus',
    '/data/account/isSplitRatio',
    '/data/account/registeredUsers',
    '/data/account/routingParams',
    '/data/account/OptionPremiumPaid',
    '/data/account/OptionPremiumRcvd',
    '/data/account/LongOptionMarketValue',
    '/data/account/ShortOptionMarketValue',
    '/data/account/MarginCallAge',
    '/data/account/MarginCallValue',
    '/data/account/StartOfDayNetLiquidationValue',
    '/data/account/ChangeAccountBalance'
]

json_get_entities_filters = [
    '/data/positions/*/lastPrice',
    '/data/positions/*/settlePrice',
    '/data/positions/*/oteM2S'
]

json_filter_data = [
    ('/account-data', json_account_data_filters),
    ('/get_entities', json_get_entities_filters)
]

server_cert_file = '/app/web-cache/cert.crt'
server_key_file = '/app/web-cache/private.key'
