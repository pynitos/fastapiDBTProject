from fastapi.security import HTTPBearer

security = HTTPBearer(bearerFormat="JWT", scheme_name="Bearer", description="JWT token from User Service.")
