import pprint
import time
from pubnub.pubnub import PubNub 
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback


class Listener(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pprint(presence.__dict__)

    def message(self, pubnub, message):
        print(f'incoming message -- {message.channel} | {message.message}')

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-9f0c2442-6789-11ec-8481-8a57b2c2a271'
pnconfig.publish_key = 'pub-c-594a87f2-c3a7-4069-9264-e35c9431b70f'
TEST_CHANNEL = 'TEST_CHANNEL'


class PubSub():
    """
    Handles functionality of publish/subcribe layer of application.
    Porvides communication between all the nodes on the blockchain network
    """

    def __init__(self) -> None:
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(TEST_CHANNEL, {'foo': 'bar'})

if __name__ == '__main__':
    main()

