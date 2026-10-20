null
DEPOSIT_RESULT = {
  "type": "object",
  "properties": {
    "code": { "type": "integer" },
    "message": {"type": "string"}，
    "data": {
      "type": "object",
      "properties": {
        "amount": { "type": "number", "minimum": 0 }
      },
      "required": ["amount"]
    },

  },
  "required": ["code", "message","data"]
}