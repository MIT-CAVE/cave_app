def get_access(globals, user):
    try:
        if user.is_staff:
            return {"access": True}
        if globals.require_email_validation:
            if not user.email_validated:
                return {
                    "access": False,
                    "link": "/",
                    "warning_page": "email_validation",
                }
        if globals.use_status_acceptance:
            if user.status == "accepted":
                return {"access": True}
            if user.status == "pending":
                return {
                    "access": False,
                    "link": "/",
                    "warning_page": "access_pending",
                }
            if user.status == "rejected":
                return {
                    "access": False,
                    "link": "/",
                    "warning_page": "access_rejected",
                }
        else:
            return {"access": True}
    except:
        pass
    return {"access": False, "link": "/"}
