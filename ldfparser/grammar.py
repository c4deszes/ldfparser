from lark import Transformer

class LdfTransformer(Transformer):
    # pylint: disable=missing-function-docstring,no-self-use,too-many-public-methods,unused-argument
    """
    Transforms the LDF grammar into a Python dictionary
    """

    def parse_integer(self, value: str):
        try:
            return int(value)
        except ValueError:
            return int(value, 16)

    def parse_real_or_integer(self, value: str):
        return float(value)

    def ldf_identifier(self, tree):
        return tree[0][0:]

    def ldf_version(self, tree):
        return tree[0][0:]

    def ldf_integer(self, tree):
        return self.parse_integer(tree[0])

    def ldf_float(self, tree):
        return self.parse_real_or_integer(tree[0])

    def ldf_channel_name(self, tree):
        # This gets rid of quote marks
        return tree[0][1:-1]

    def start(self, tree):
        return tree[0]

    def ldf(self, tree):
        ldf = {}
        for k in tree[0:]:
            ldf[k[0]] = k[1]
        return ldf

    def header_lin_description_file(self, tree):
        return ("header", "lin_description_file")

    def header_protocol_version(self, tree):
        return ("protocol_version", tree[0])

    def header_language_version(self, tree):
        return ("language_version", tree[0])

    def header_speed(self, tree):
        return ("speed", int(float(tree[0]) * 1000))

    def header_channel(self, tree):
        return ("channel_name", tree[0])

    def nodes(self, tree):
        if len(tree) == 0:
            return ("nodes", {})
        if len(tree) == 1:
            return ("nodes", {'master': tree[0]})
        return ("nodes", {'master': tree[0], 'slaves': tree[1]})

    def nodes_master(self, tree):
        return {"name": tree[0], "timebase": tree[1] * 0.001, "jitter": tree[2] * 0.001}

    def nodes_slaves(self, tree):
        return tree

    def node_compositions(self, tree):
        return ("node_compositions", tree[0:])

    def node_compositions_configuration(self, tree):
        return {"name": tree[0], "compositions": tree[1]}

    def node_compositions_composite(self, tree):
        return {"name": tree[0], "nodes": tree[1:]}

    def signals(self, tree):
        return ("signals", tree)

    def signal_definition(self, tree):
        return {"name": tree[0], "width": int(tree[1]), "init_value": tree[2], "publisher": tree[3], "subscribers": tree[4:]}

    def signal_default_value(self, tree):
        return tree[0]

    def signal_default_value_single(self, tree):
        return tree[0]

    def signal_default_value_array(self, tree):
        return tree[0:]

    def diagnostic_signals(self, tree):
        return ("diagnostic_signals", tree)

    def diagnostic_signal_definition(self, tree):
        return {"name": tree[0], "width": int(tree[1]), "init_value": tree[2]}

    def frames(self, tree):
        return ("frames", tree)

    def frame_definition(self, tree):
        return {"name": tree[0], "frame_id": int(tree[1]), "publisher": tree[2], "length": tree[3] if len(tree) > 4 else None, "signals": tree[4] if len(tree) > 4 else tree[3]}

    def frame_signals(self, tree):
        return tree[0:]

    def frame_signal(self, tree):
        return {"signal": tree[0], "offset": int(tree[1])}

    def sporadic_frames(self, tree):
        return ("sporadic_frames", tree[0:])

    def sporadic_frame_definition(self, tree):
        return {"name": tree[0], "frames": tree[1:]}

    def event_triggered_frames(self, tree):
        return ("event_triggered_frames", tree[0:])

    def event_triggered_frame_definition(self, tree):
        return {"name": tree[0], "collision_resolving_schedule_table": tree[1], "frame_id": tree[2], "frames": tree[3]}

    def event_triggered_frame_definition_frames(self, tree):
        return tree[0:]

    def diagnostic_frames(self, tree):
        return ("diagnostic_frames", tree)

    def diagnostic_frame_definition(self, tree):
        return {"name": tree[0], "frame_id": int(tree[1]), "signals": tree[2]}

    def diagnostic_frame_signals(self, tree):
        return tree[0:]

    def diagnostic_addresses(self, tree):
        return ("diagnostic_addresses", dict(tree))

    def diagnostic_address(self, tree):
        return (tree[0], tree[1])

    def node_attributes(self, tree):
        return ("node_attributes", tree[0:])

    def node_definition(self, tree):
        node = {"name": tree[0]}
        for k in tree[1:]:
            node[k[0]] = k[1]
        return node

    def node_definition_protocol(self, tree):
        return ("lin_protocol", tree[0])

    def node_definition_configured_nad(self, tree):
        return ("configured_nad", tree[0])

    def node_definition_initial_nad(self, tree):
        return ("initial_nad", tree[0])

    def node_definition_product_id(self, tree):
        return ("product_id", {"supplier_id": tree[0], "function_id": tree[1], "variant": tree[2] if len(tree) > 2 else 0})

    def node_definition_response_error(self, tree):
        return ("response_error", tree[0])

    def node_definition_fault_state_signals(self, tree):
        return ("fault_state_signals", tree[0:])

    def node_definition_p2_min(self, tree):
        return ("P2_min", tree[0] * 0.001)

    def node_definition_st_min(self, tree):
        return ("ST_min", tree[0] * 0.001)

    def node_definition_n_as_timeout(self, tree):
        return ("N_As_timeout", tree[0] * 0.001)

    def node_definition_n_cr_timeout(self, tree):
        return ("N_Cr_timeout", tree[0] * 0.001)

    def node_definition_configurable_frames(self, tree):
        return tree[0]

    def node_definition_configurable_frames_20(self, tree):
        frames = {}
        value = iter(tree)
        for frame, msg_id in zip(value, value):
            frames[frame] = msg_id
        return ("configurable_frames", frames)

    def node_definition_configurable_frames_21(self, tree):
        return ("configurable_frames", tree[0:])

    def schedule_tables(self, tree):
        return ("schedule_tables", tree)

    def schedule_table_definition(self, tree):
        return {"name": tree[0], "schedule": tree[1:]}

    def schedule_table_entry(self, tree):
        return {"command": tree[0], "delay": tree[1] * 0.001}

    def schedule_table_command(self, tree):
        return tree[0]

    def schedule_table_command_masterreq(self, tree):
        return {"type": "master_request"}

    def schedule_table_command_slaveresp(self, tree):
        return {"type": "slave_response"}

    def schedule_table_command_assignnad(self, tree):
        return {"type": "assign_nad", "node": tree[0]}

    def schedule_table_command_conditionalchangenad(self, tree):
        return {"type": "conditional_change_nad", "nad": tree[0], "id": tree[1], "byte": tree[2], "mask": tree[3], "inv": tree[4], "new_nad": tree[5]}

    def schedule_table_command_datadump(self, tree):
        return {"type": "data_dump", "node": tree[0], "data": tree[1:]}

    def schedule_table_command_saveconfiguration(self, tree):
        return {"type": "save_configuration", "node": tree[0]}

    def schedule_table_command_assignframeidrange(self, tree):
        return {"type": "assign_frame_id_range", "node": tree[0], "frame_index": tree[1], "pids": tree[2:]}

    def schedule_table_command_assignframeid(self, tree):
        return {"type": "assign_frame_id", "node": tree[0], "frame": tree[1]}

    def schedule_table_command_unassignframeid(self, tree):
        return {"type": "unassign_frame_id", "node": tree[0], "frame": tree[1]}

    def schedule_table_command_freeformat(self, tree):
        return {"type": "free_format", "data": tree[0:]}

    def schedule_table_command_frame(self, tree):
        return {"type": "frame", "frame": tree[0]}

    def signal_groups(self, tree):
        return ("signal_groups", tree)

    def signal_group(self, tree):
        signals = {}
        value = iter(tree[2:])
        for signal, offset in zip(value, value):
            signals[signal] = offset
        return {"name": tree[0], "size": tree[1], "signals": signals}

    def signal_encoding_types(self, tree):
        return ("signal_encoding_types", tree)

    def signal_encoding_type(self, tree):
        return {"name": tree[0], "values": tree[1:]}

    def signal_encoding_logical_value(self, tree):
        return {"type": "logical", "value": tree[0], "text": tree[1] if len(tree) > 1 else None}

    def signal_encoding_physical_value(self, tree):
        return {"type": "physical", "min": tree[0], "max": tree[1], "scale": tree[2], "offset": tree[3], "unit": tree[4] if len(tree) > 4 else None}

    def signal_encoding_bcd_value(self, tree):
        return {"type": "bcd"}

    def signal_encoding_ascii_value(self, tree):
        return {"type": "ascii"}

    def signal_encoding_text_value(self, tree):
        return tree[0][1:-1]

    def signal_representations(self, tree):
        return ("signal_representations", tree)

    def signal_representation_node(self, tree):
        return {"encoding": tree[0], "signals": tree[1:]}
