import os
from pysui import SuiConfig
from dotenv import load_dotenv
from pysui import AsyncClient, SuiConfig, handle_result
from pysui.sui.sui_txn import AsyncTransaction
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_txresults.single_tx import SuiCoinObject

# Load environment variables
load_dotenv()

async def get_sui_client():
    config = SuiConfig.user_config(
        prv_keys=[os.getenv("SUI_PRIVATE_KEY")], 
        rpc_url=os.getenv("SUI_RPC_URL"), 
        ws_url="wss://fullnode.devnet.sui.io:443"
    )
    client = AsyncClient(config)
    return client

async def send_transaction(client: AsyncClient, recipient_address, amount):
    try:
        # Example transaction (you need to adjust with actual Sui API call)
        txn = AsyncTransaction(client=client)
        ownerAddress = client.config.addresses[0]
        ownerObjects = await client.get_objects(ownerAddress)
        if not coinObject.is_ok():
            raise Exception(f"Failed to retrieve objects: {coinObject}")
        coinObject = ownerObjects.result_data.data[0]
        coinSui = SuiCoinObject(
            coin_type=coinObject.object_type, 
            coin_object_id=coinObject.object_id, 
            version=coinObject.version, 
            digest=coinObject.digest, 
            balance=coinObject.balance, 
            previous_transaction=coinObject.previous_transaction
        )

        some_recipient = SuiAddress(recipient_address)

        # Split the coin and transfer objects (async)
        split_result = await txn.split_coin(coin=coinSui, amounts=[amount])
        await txn.transfer_objects(
            transfers=[split_result],
            recipient=some_recipient,
        )

        # Execute the transaction (async) with a gas budget
        tx_result = await txn.execute(gas_budget=30000000)
        return handle_result(tx_result)
    except Exception as e:
        raise Exception(f"Transaction failed: {str(e)}")
