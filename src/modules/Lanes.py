class Lane:
    # from \\scenario\\in\\most.net.xml
    def __init__(self, lane_id, index, speed, allow=None, disallow=None, length=None, width=None, shape=None):
        """
        :param lane_id: unique name - String example - "131316_w0"
        :param index:   number of road lanes start at 0 - String example "0"
        :param allow:   allow or not passageway - String example - "pedestrian"
        :param speed:   lane speed m/s String example - "1.00"
        :param length:  lane length meters String example - "5.10", default = None
        :param width:   lane width meters String example - "2.00", default = None
        :param shape:   lane shape - String, default = None
        """
        self.lane_id = lane_id
        self.index = index
        self.allow = allow
        self.disallow = disallow
        self.speed = speed
        self.length = length
        self.width = width
        self.shape = shape
        self.occupancy = None

    @staticmethod
    def subscribe_argument():
        return {
            "last_step_occupancy": {
                "hex": 0x13
            },
        }

    def update_attribute(self, subscribed_result, interval_size, current_interval):
        if not self.occupancy:
            self.occupancy = [0] * interval_size

        argument_to_update = Lane.subscribe_argument()["last_step_occupancy"]['hex']
        if subscribed_result[argument_to_update] > 0.0:
            try:
                print('Updating lane id:', self.lane_id, 'subscribed_result: ', 'current occupancy: ',
                      self.occupancy[current_interval])
                self.occupancy[current_interval] = (self.occupancy[current_interval] +
                                                    subscribed_result[argument_to_update]) / 2
                print('subscribe occupancy: ', subscribed_result[argument_to_update], 'current_interval',
                      current_interval, 'new occupancy: ', self.occupancy[current_interval], "\n\n")

            except KeyError as e:
                print('I got a KeyError - reason "%s"' % str(e))
                print('subscribed_result ', subscribed_result)
                exit(0)
