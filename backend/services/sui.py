import os
from pysui import SuiConfig
from dotenv import load_dotenv
from pysui import AsyncClient, SuiConfig, handle_result
from pysui.sui.sui_txn import AsyncTransaction
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_txresults.single_tx import SuiCoinObject
import logging

# Load environment variables
load_dotenv()

async def get_sui_client():
    logging.info(f"The private key {os.getenv('SUI_PRIVATE_KEY')}")
    logging.info(f"The rpc url {os.getenv('SUI_RPC_URL')}")
    config = SuiConfig.user_config(
        prv_keys=[os.getenv('SUI_PRIVATE_KEY')], 
        rpc_url=os.getenv('SUI_NODE_URL'), 
        ws_url='wss://fullnode.devnet.sui.io:443'
    )
    client = AsyncClient(config)
    return client

async def send_transaction(client: AsyncClient, recipient_address, amount):
    try:
        logging.info("Starting transaction process")
        
        # Start transaction and log the owner address
        txn = AsyncTransaction(client=client)
        ownerAddress = client.config.addresses[0]
        logging.info(f"Owner address: {ownerAddress}")

        # Fetch the owner's objects
        logging.info(f"Fetching objects for owner: {ownerAddress}")
        ownerObjects = await client.get_objects(ownerAddress)
        if not ownerObjects.is_ok():
            raise Exception(f"Failed to retrieve objects: {ownerObjects}")

        # Log available objects
        logging.info(f"Owner objects retrieved: {ownerObjects.result_data}")

        # Select the first coin object and log its details
        coinObject = ownerObjects.result_data.data[0]
        logging.info(f"Selected coin object: {coinObject.object_id}")

        # Create a SuiCoinObject and log it
        coinSui = SuiCoinObject(
            coin_type=coinObject.object_type, 
            coin_object_id=coinObject.object_id, 
            version=coinObject.version, 
            digest=coinObject.digest, 
            balance=coinObject.balance, 
            previous_transaction=coinObject.previous_transaction
        )
        logging.info(f"Created SuiCoinObject: {coinSui}")

        # Log the recipient address
        some_recipient = SuiAddress(recipient_address)
        logging.info(f"Recipient address: {some_recipient}")

        # Split the coin and log the result
        logging.info(f"Splitting coin for amount: {amount}")
        split_result = await txn.split_coin(coin=coinSui, amounts=[amount])
        logging.info(f"Coin split result: {split_result}")

        # Transfer the split coin to the recipient and log it
        logging.info(f"Transferring split coin to recipient: {recipient_address}")
        await txn.transfer_objects(
            transfers=[split_result],
            recipient=some_recipient,
        )

        # Execute the transaction and log the gas budget
        logging.info("Executing transaction with gas budget: 30000000")
        tx_result = await txn.execute(gas_budget=30000000)

        # Log the transaction result
        logging.info(f"Transaction executed successfully: {handle_result(tx_result)}")
        return handle_result(tx_result)

    except Exception as e:
        logging.error(f"Transaction failed: {str(e)}")
        raise Exception(f"Transaction failed: {str(e)}")
