class StatusCode:
    undefined = 0
    empty = 10
    ready = 20
    started = 30
    finished = 40
    cancelled = 100
    rate_limited = 110
    error = 1000

    label = {
        undefined: "Undefined",
        empty: "Empty",
        ready: "Ready",
        started: "Started",
        finished: "Finished",
        cancelled: "Cancelled",
        rate_limited: "Rate limited",
        error: "Error",
    }

    @staticmethod
    def is_errored(code):
        return code >= StatusCode.error

    @staticmethod
    def code_to_label(code):
        return StatusCode.label.get(code, "Unknown StatusCode")
