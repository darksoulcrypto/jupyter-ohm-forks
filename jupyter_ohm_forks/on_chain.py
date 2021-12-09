import math
from web3 import Web3
import pandas as pd

def add_on_chain_data(df):
    """
    - metrics
      - BCV
      - index
      - supply
      - growth
      - dilution
      - stakedAmount
      - rebase
      - APY
    - todo
      - DCV?
    """

    on_chain_data = []

    for idx, row in df.iterrows():
        w3 = Web3(Web3.HTTPProvider(row['api']))

        token_abi = open(f"abis/{row['token_ticker']}.abi", "r").read()
        staked_abi = open(f"abis/{row['staked_ticker']}.abi", "r").read()
        staking_abi = open(f"abis/{row['staked_ticker']}staking.abi", "r").read()

        token_contract = w3.eth.contract(Web3.toChecksumAddress(row['token_contract']), abi=token_abi)
        staked_contract = w3.eth.contract(Web3.toChecksumAddress(row['staked_contract']), abi=staked_abi)
        staking_contract = w3.eth.contract(Web3.toChecksumAddress(row['staking_contract']), abi=staking_abi)

        data = {}
        data['oc_token_ticker'] = row['token_ticker']

        """
        #marketPrice = ((await getMarketPrice(networkID, provider)) / Math.pow(10, 9)) * mimPrice;

        data['oc_total_supply'] = token_contract.functions.totalSupply().call() / math.pow(10, 9)
        data['oc_circ_supply'] = staked_contract.circulatingSupply().call() / math.pow(10, 9)

        data['oc_staking_tvl'] = data['oc_circ_supply'] * market_price
        data['oc_market_cap'] = data['oc_total_supply'] * market_price

        const tokenBalPromises = allBonds.map(bond => bond.getTreasuryBalance(networkID, provider));
        const tokenBalances = await Promise.all(tokenBalPromises);
        const treasuryBalance = tokenBalances.reduce((tokenBalance0, tokenBalance1) => tokenBalance0 + tokenBalance1);

        const tokenAmountsPromises = allBonds.map(bond => bond.getTokenAmount(networkID, provider));
        const tokenAmounts = await Promise.all(tokenAmountsPromises);
        const rfvTreasury = tokenAmounts.reduce((tokenAmount0, tokenAmount1) => tokenAmount0 + tokenAmount1);

        const sbBondsAmountsPromises = allBonds.map(bond => bond.getSbAmount(networkID, provider));
        const sbBondsAmounts = await Promise.all(sbBondsAmountsPromises);
        const sbAmount = sbBondsAmounts.reduce((sbAmount0, sbAmount1) => sbAmount0 + sbAmount1, 0);
        const sbSupply = totalSupply - sbAmount;

        rfv = treasury_balance / total_supply
        """

        epoch = staking_contract.functions.epoch().call()
        staking_reward = epoch[3]
        circ = staked_contract.functions.circulatingSupply().call()
        staking_rebase = staking_reward / circ
        data["oc_five_day_rate"] = math.pow(1 + staking_rebase, 5 * 3) - 1
        data["oc_staking_apy"] = math.pow(1 + staking_rebase, 365 * 3) - 1

        current_index = staking_contract.functions.index().call()
        data["oc_next_rebase"] = epoch[2]
        """
        treasury_runway = rfv_treasury / circ_supply
        runway = math.log(treasury_runway) / math.log(1 + staking_rebase) / 3
        """
        on_chain_data.append(data)

    df_new = pd.DataFrame(on_chain_data)
    return pd.merge(df, df_new, left_on="token_ticker", right_on="oc_token_ticker")