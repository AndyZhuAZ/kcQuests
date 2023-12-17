class Mission:
    def __init__(self, req_times, times, battle_map=None, battle_result=None, operation_id=None, destroy_item=None):
        self.req_times = req_times
        self.times = times
        self.battle_map = battle_map
        self.battle_result = battle_result
        self.operation_id = operation_id
        self.destroy_item = destroy_item

    def to_conning_tower_format(self):
        """
        Generates a dictionary in the Conning Tower format.
        dart class:
        QuestMission({
          required int reqTimes,
          required int times,
          int? battleMap,
          int? battleResult,
          int? operationId,
          int? destroyItem,
        })

        Returns: dict
        """
        if (self.battle_map is not None) and (self.battle_result is not None):
            return {
                'reqTimes': self.req_times,
                'times': self.times,
                'battleMap': self.battle_map,
                'battleResult': self.battle_result,
            }
        if self.operation_id is not None:
            return {
                'reqTimes': self.req_times,
                'times': self.times,
                'operationId': self.operation_id,
            }
        if self.destroy_item is not None:
            return {
                'reqTimes': self.req_times,
                'times': self.times,
                'destroyItem': self.destroy_item,
            }

        return {
            'reqTimes': self.req_times,
            'times': self.times,
        }


