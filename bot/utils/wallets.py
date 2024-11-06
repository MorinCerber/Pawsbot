import os
import sys
import json

from bot.utils import logger
from bot.config import settings

from tonsdk.contract.wallet import Wallets, WalletVersionEnum

def get_used_wallets():
    file_path = 'used_wallet.json'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

    with open(file_path, 'r') as file:
        used_wallets = json.load(file)

    return used_wallets

def generate_wallets(count):
    file_path = 'wallet.json'

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

    with open(file_path, 'r') as file:
        wallets = json.load(file)

    for i in range(1, count + 1):
        mnemonics, pub_k, priv_k, wallet = Wallets.create(WalletVersionEnum.v4r2, workchain=0)
        wallet_address = wallet.address.to_string(True, True, False)

        wallets.update(
            {
                wallet_address: " ".join(mnemonics)
            }
        )

        logger.success(f"Created wallet {i}/{count}")

    with open('wallet.json', 'w') as file:
        json.dump(wallets, file, indent=4)

def get_wallets():
    if os.path.exists("wallet.json"):
        used_wallets = list(get_used_wallets().keys())
        with open("wallet.json", "r") as f:
            wallets = json.load(f)

        if len(wallets) == 0 and settings.ENABLE_CHECKER:
            logger.warning("<yellow>TO CONNECT WALLET YOU MUST GENERATE WALLET USING OPTION 3 FIRST!</yellow>")
            sys.exit()

        need_to_del = []

        for wallet in wallets.keys():
            if wallet in used_wallets:
                need_to_del.append(wallet)

        for wallet in need_to_del:
            del wallets[wallet]
        # print(wallets)
        return wallets
    else:
        if settings.ENABLE_CHECKER:
            logger.warning("<yellow>TO CONNECT WALLET YOU MUST GENERATE WALLET USING OPTION 3 FIRST!</yellow>")
            sys.exit()
