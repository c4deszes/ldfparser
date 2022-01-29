import os
import pytest

from ldfparser.parser import parse_ldf
from ldfparser.schedule import AssignNadEntry, ConditionalChangeNadEntry, SaveConfigurationEntry

class TestSchedule:

    @pytest.mark.unit
    def test_schedule_load(self):
        path = os.path.join(os.path.dirname(__file__), "ldf", "lin_schedules.ldf")
        ldf = parse_ldf(path)

        assert len(ldf.get_schedule_tables()) == 5
        
        address_config_table = ldf.get_schedule_table('AddressConfiguration_Schedule')
        assert len(address_config_table.schedule) == 5

        entry_1 = address_config_table.schedule[0]
        assert isinstance(entry_1, AssignNadEntry)
        assert entry_1.delay == 10
        assert entry_1.node.name == 'LeftLight'

        entry_2 = address_config_table.schedule[1]
        assert isinstance(entry_2, SaveConfigurationEntry)
        assert entry_2.delay == 10
        assert entry_2.node.name == 'LeftLight'

        entry_5 = address_config_table.schedule[4]
        assert isinstance(entry_5, ConditionalChangeNadEntry)
        assert entry_5.delay == 10
        assert entry_5.nad == 0x7F
        assert entry_5.id == 0x01
        assert entry_5.byte == 0x03
        assert entry_5.mask == 0x01
        assert entry_5.inv == 0xFF
        assert entry_5.new_nad == 0x01
