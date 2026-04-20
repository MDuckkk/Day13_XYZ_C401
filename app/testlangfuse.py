from langfuse import get_client, observe

langfuse = get_client()
print("auth_check =", langfuse.auth_check())

@observe()
def test():
    return {"ok": True}

test()
langfuse.flush()
print("done")