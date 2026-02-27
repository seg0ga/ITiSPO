
def next_state(state: str, event: str) -> str:
    if state=="NEW":
        if event=="PAY_OK":return "PAID"
        elif event=="PAY_FAIL":return "CANCELLED"
    elif state=="PAID":
        if event=="complete":return "DONE"
        elif event=="cancel" or event=="fail":return "CANCELLED"
    elif state=="DONE":return "DONE"
    elif state=="CANCELLED":return "CANCELLED"

    return state