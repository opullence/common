class StatusCode():
    undefined = 0
    empty = 10
    ready = 20
    started = 30
    finished = 40
    error = 100
    cancelled = 200
    rate_limited = 300

    label = {
        undefined: "Undefined",
        empty: "Empty",
        ready: "Ready",
        started: "Started",
        finished: "Finished",
        error: "Error",
        cancelled: "Cancelled",
        rate_limited: "Rate limited",
    }

    @staticmethod
    def is_errored(code):
        return code >= StatusCode.error

    @staticmethod
    def code_to_label(code):
        return StatusCode.label.get(code, "Unknown StatusCode")
