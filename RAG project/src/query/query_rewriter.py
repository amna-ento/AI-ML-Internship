def rewrite_query(query):
    query = query.strip().lower()

    replacements = {
        "what about emergency contacts":
            "employee emergency contact update requirements",

        "how quickly do i need to report a change":
            "employee information change reporting deadline",

        "can my manager change my record":
            "manager authority to change employee personnel records",

        "what documents do i need":
            "required supporting documents for employee information changes",

        "how much leave i can get anually":
            "annual leave entitlement for employees"
    }

    return replacements.get(query, query)