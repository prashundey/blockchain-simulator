from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-9f0c2442-6789-11ec-8481-8a57b2c2a271'
pnconfig.publish_key = 'pub-c-594a87f2-c3a7-4069-9264-e35c9431b70f'
pnconfig.uuid = 'myUniqueUUID'
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('my_channel2').message({'foo': 'bar'}).pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('my_channel2').execute()



# from pubnub.callbacks import SubscribeCallback
# from pubnub.enums import PNStatusCategory
# from pubnub.pnconfiguration import PNConfiguration
# from pubnub.pubnub import PubNub
# from pprint import pprint

# class Listener(SubscribeCallback):
#     def status(self, pubnub, status):
#         pass

#     def presence(self, pubnub, presence):
#         pprint(presence.__dict__)

#     def message(self, pubnub, message):
#         pprint(message.__dict__)

# def my_publish_callback(envelope, status):

#     print(envelope, status)

# pnconfig = PNConfiguration()
# pnconfig.subscribe_key = "sub-c-9f0c2442-6789-11ec-8481-8a57b2c2a271"
# pnconfig.publish_key = "pub-c-594a87f2-c3a7-4069-9264-e35c9431b70f"

# pubnub = PubNub(pnconfig)
# pubnub.add_listener(Listener())

# pubnub.subscribe()\
#     .channels("Test-Channel")\
#     .with_presence()\
#     .execute()\

# pubnub.publish()\
#     .channel("Test-Channel")\
#     .message({'foo' : 'bar'})\
#     .pn_async(my_publish_callback)
