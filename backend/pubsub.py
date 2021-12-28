# import time
# from pubnub.pubnub import PubNub 
# from pubnub.pnconfiguration import PNConfiguration
# from pubnub.callbacks import SubscribeCallback

# class Listener(SubscribeCallback):
#     """
#     """
#     def message(self, pubnub, message):
#         print(f'\n-- incoming message: {message}')
#         #return super().message(pubnub, message)



# pnconfig = PNConfiguration()
# pnconfig.subscribe_key = 'sub-c-9f0c2442-6789-11ec-8481-8a57b2c2a271'
# pnconfig.publish_key = 'pub-c-594a87f2-c3a7-4069-9264-e35c9431b70f'

# pubnub = PubNub(pnconfig)

# pubnub.add_listener(Listener())

# TEST_CHANNEL = 'TEST_CHANNEL'
# pubnub.subscribe().channels([TEST_CHANNEL]).execute()


# def my_publish_callback(envelope, status):
#     print(envelope)
#     print(envelope, status)

# def main():
#     time.sleep(1)
#     pubnub.publish().channel([TEST_CHANNEL]).message({'foo': 'bar'}).pn_async(my_publish_callback)
    

# if __name__ == "__main__":
#     main()

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint

class Listener(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pprint(presence.__dict__)

    def message(self, pubnub, message):
        pprint(message.__dict__)

def my_publish_callback(envelope, status):
    print(envelope, status)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-9f0c2442-6789-11ec-8481-8a57b2c2a271"
pnconfig.publish_key = "pub-c-594a87f2-c3a7-4069-9264-e35c9431b70f"

pubnub = PubNub(pnconfig)
pubnub.add_listener(Listener())

pubnub.subscribe()\
    .channels("Test-Channel")\
    .with_presence()\
    .execute()\

pubnub.publish()\
    .channel("Test-Channel")\
    .message({'foo' : 'bar'})\
    .pn_async(my_publish_callback)