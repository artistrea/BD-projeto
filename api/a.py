from jsonschema import validate

validate(instance={"email": "ava@ava"}, schema={
    "type": "object",
    "properties": {
        "email": { "type": "number" },
        "password": { "type": "string" },
    },
})
print("deu certo mas n era pra dar")
