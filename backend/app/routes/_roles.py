import json
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort

def require_roles(*allowed):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            ident_raw=get_jwt_identity()
            try: ident=json.loads(ident_raw)
            except Exception: abort(401, message="Invalid token identity payload")
            role=ident.get("role","lectura"); order={"lectura":1,"editor":2,"admin":3}
            if max(order.get(r,0) for r in allowed) > order.get(role,0):
                abort(403, message="Insufficient role")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
