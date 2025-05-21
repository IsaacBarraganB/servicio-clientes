import inspect
from project import schemas

clases = [obj for name, obj in inspect.getmembers(schemas, inspect.isclass)]

def schemas_openapi_config(schema):
    classes = clases
    schemas = {}
    for clase in classes:
        if clase.__name__ != "BaseModel":
            schemas[clase.__name__] = clase.model_json_schema()
    schemas["HTTPValidationError"] = {
        "title": "HTTPValidationError",
        "type": "object",
        "properties": {
            "detail": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "loc": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "msg": {
                            "type": "string"
                        },
                        "type": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
    schemas["ValidationError"] = {
        "title": "ValidationError",
        "type": "object",
        "properties": {
            "loc": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "msg": {
                "type": "string"
            },
            "type": {
                "type": "string"
            }
        }
    }
    schema["schemas"] = schemas
    return schema

""" "schemas": {
        "UserSchema": UserSchema.model_json_schema(),
        "Token": Token.model_json_schema(),
        "Message": Message.model_json_schema(),
        "OAuth2PasswordRequestForm": OAuth2PasswordRequestFormSchema.model_json_schema(),
        "HTTPValidationError": {
            "title": "HTTPValidationError",
            "type": "object",
            "properties": {
                "detail": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "loc": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "msg": {
                                "type": "string"
                            },
                            "type": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        },
        "ValidationError": {
            "title": "ValidationError",
            "type": "object",
            "properties": {
                "loc": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "msg": {
                    "type": "string"
                },
                "type": {
                    "type": "string"
                }
            }
        },
    }



 """
