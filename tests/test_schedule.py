import os
import pytest

from ldfparser.parser import parse_ldf
from ldfparser.schedule import AssignFrameIdEntry, AssignFrameIdRangeEntry, AssignNadEntry, ConditionalChangeNadEntry, DataDumpEntry, FreeFormatEntry, LinFrameEntry, MasterRequestEntry, SaveConfigurationEntry, SlaveResponseEntry, UnassignFrameIdEntry

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
        assert entry_1.delay == 0.010
        assert entry_1.node.name == 'LeftLight'

        entry_2 = address_config_table.schedule[1]
        assert isinstance(entry_2, SaveConfigurationEntry)
        assert entry_2.delay == 0.010
        assert entry_2.node.name == 'LeftLight'

        entry_5 = address_config_table.schedule[4]
        assert isinstance(entry_5, ConditionalChangeNadEntry)
        assert entry_5.delay == 0.010
        assert entry_5.nad == 0x7F
        assert entry_5.id == 0x01
        assert entry_5.byte == 0x03
        assert entry_5.mask == 0x01
        assert entry_5.inv == 0xFF
        assert entry_5.new_nad == 0x01

        frame_config_table = ldf.get_schedule_table('FrameConfiguration_Schedule')
        assert len(frame_config_table.schedule) == 8

        entry_1 = frame_config_table.schedule[0]
        assert isinstance(entry_1, AssignFrameIdRangeEntry)
        assert entry_1.node.name == 'LeftLight'
        assert entry_1.frame_index == 0
        assert entry_1.pids == [0x40, 0x42, 0xFF, 0xFF]

        entry_5 = frame_config_table.schedule[4]
        assert isinstance(entry_5, AssignFrameIdEntry)
        assert entry_5.node.name == 'LeftLight'
        assert entry_5.frame.name == 'LeftLightStatus'

        entry_6 = frame_config_table.schedule[5]
        assert isinstance(entry_6, UnassignFrameIdEntry)
        assert entry_6.node.name == 'LeftLight'
        assert entry_6.frame.name == 'LeftLightStatus'

        information_schedule = ldf.get_schedule_table('InformationSchedule')
        assert len(information_schedule.schedule) == 3

        entry_1 = information_schedule.schedule[0]
        assert isinstance(entry_1, DataDumpEntry)
        assert entry_1.node.name == 'LeftLight'
        assert entry_1.data == [0x10, 0x80, 0x00, 0xFF, 0xFF]

        entry_3 = information_schedule.schedule[2]
        assert isinstance(entry_3, FreeFormatEntry)
        assert entry_3.data == [0x3C, 0xB2, 0x00, 0x00, 0xFF, 0x7F, 0xFF, 0xFF]

        diagnostic_schedule = ldf.get_schedule_table('Diagnostic_Schedule')
        assert len(diagnostic_schedule.schedule) == 2

        entry_1 = diagnostic_schedule.schedule[0]
        assert isinstance(entry_1, MasterRequestEntry)

        entry_2 = diagnostic_schedule.schedule[1]
        assert isinstance(entry_2, SlaveResponseEntry)

        normal_schedule = ldf.get_schedule_table('Normal_Schedule')
        assert len(normal_schedule.schedule) == 4

        entry_1 = normal_schedule.schedule[0]
        assert isinstance(entry_1, LinFrameEntry)
        assert entry_1.frame.name == 'LeftLightSet'
