import pprint
import time
from pubnub.pubnub import PubNub 
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

CHANNELS = {
    'TEST' : 'TEST',
    'BLOCK' : 'BLOCK'
}

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-9f0c2442-6789-11ec-8481-8a57b2c2a271'
pnconfig.publish_key = 'pub-c-594a87f2-c3a7-4069-9264-e35c9431b70f'


class Listener(SubscribeCallback):
    """
    Custom listener for listening to channel, recieving broadcasts, 
    and modifying local instance blockchain if necessary
    """
    def __init__(self, blockchain : Blockchain) -> None:
        self.blockchain = blockchain


    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pprint(presence.__dict__)

    def message(self, pubnub, message):
        print(f'incoming message -- {message.channel} Channel')
        print(message.message)

        if message.channel == CHANNELS['BLOCK']:
            new_block = Block.from_json(message.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(new_block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n --- Succesfully replaced local chain')
            except Exception as e:
                print(f'\n --- Did not replace chain {e}')


class PubSub():
    """
    Handles functionality of publish/subcribe layer of application.
    Porvides communication between all the nodes on the blockchain network
    """

    def __init__(self, blockchain : Blockchain) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block : Block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})

if __name__ == '__main__':
    main()

