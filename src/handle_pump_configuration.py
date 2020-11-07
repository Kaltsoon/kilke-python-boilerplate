from persisted_run_pump import persisted_run_pump


def handle_pump_configuration(payload, on_ack, on_fault):
    type = payload['type']
    rpm = payload['rpm']

    if rpm == None:
        return

    result = persisted_run_pump(type, rpm)

    if result == '':
        on_fault()
    else:
        on_ack(type, rpm)
