TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression such as 4500 + 1200"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to another using live exchange rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Amount to convert"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "Three-letter source currency code such as USD"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "Three-letter target currency code such as PKR"
                    }
                },
                "required": [
                    "amount",
                    "from_currency",
                    "to_currency"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "add_expense",
            "description": "Add a personal expense to the expense database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Expense amount"
                    },
                    "category": {
                        "type": "string",
                        "description": "Expense category such as food or transport"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the expense"
                    },
                    "date": {
                        "type": "string",
                        "description": "Expense date in YYYY-MM-DD format"
                    },
                    "currency": {
                        "type": "string",
                        "description": "Three-letter currency code"
                    }
                },
                "required": [
                    "amount",
                    "category",
                    "description",
                    "date",
                    "currency"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "query_expenses",
            "description": "Query the user's stored expenses.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Optional expense category"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Optional start date in YYYY-MM-DD format"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Optional end date in YYYY-MM-DD format"
                    }
                },
                "required": []
            }
        }
    }
]