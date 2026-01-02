import json

# Schema mínimo para validar matrices/protocolo exportados a JSON.
# Se mantiene en formato JSON (string) para evitar problemas de literales Python.
SCHEMA_JSON = """{
  "title": "RMD2 Matrix JSON",
  "type": "object",
  "required": [
    "meta"
  ],
  "properties": {
    "meta": {
      "type": "object"
    },
    "data": {
      "type": [
        "array",
        "null"
      ]
    },
    "sheets": {
      "type": [
        "object",
        "null"
      ]
    }
  },
  "additionalProperties": true
}"""
SCHEMA = json.loads(SCHEMA_JSON)
