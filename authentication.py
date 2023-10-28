"""It will handle all the Authentications and Authorizations."""


from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer()


class Authenticate:
    """Authentication class."""

    def __init__(self):
        """Initialize algorithm, secretkey, token expier time."""
        self.secret_key = (
            "9fd6b7d52e3fefaa126c7e476a7a28e0996a64a902453dc8d679cfbab86a75db"
        )
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def hash_password(self, password: str) -> str:
        """Hash the Password.

        Args:
            password (str): plain Password

        Returns:
            str: Hashed Password
        """
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password.

        Args:
            password (str): plain Password
            hashed_password (str): Hashed Password

        Returns:
            bool: password correct or not
        """
        return self.pwd_context.verify(password, hashed_password)

    def create_jwt_token(
        self, data_for_jwt: dict, expire_minutes: int | None = None
    ) -> str:
        """Create JWT token.

        Args:
            data_for_jwt (dict): data for jwt token
            expire_minutes (int | None, optional):
                expiery duration in minutes for jwt token. Defaults to None.

        Returns:
            str: JWT token created.
        """
        data_to_encode = data_for_jwt.copy()
        if expire_minutes:
            expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        data_to_encode.update({"exp": expire})
        jwt_token = jwt.encode(
            data_to_encode, key=self.secret_key, algorithm=self.algorithm
        )
        return jwt_token

    def decode_jwt_token(self, token: str) -> dict:
        """Get data from JWT token.

        Args:
            token (str): token to get data

        Raises:
            HTTPException: if token is invalid or expiered.

        Returns:
            dict: Data from jwt token
        """
        try:
            payload = jwt.decode(
                token, key=self.secret_key, algorithms=self.algorithm
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )


def get_user_data(
    request: Request,
    authorization: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    """Get data from jwt and add it to request.

    Args:
        request (Request): Request to process
        authorization (HTTPAuthorizationCredentials, optional):
            jwt token. Defaults to Depends(security).
    """
    token = authorization.credentials
    auth = Authenticate()
    user_data = auth.decode_jwt_token(token)
    request.state.user_data = user_data


def authorize(task, user_data):
    """Check whether user can edit the specified task or not.

    Args:
        task (Task): task to check access.
        user_data (User): user data to check access.

    Raises:
        HTTPException: if User can't access the task
    """
    if task.owner_id != user_data["email"]:
        raise HTTPException(
            status_code=403, detail="You are not allowed to edit this task"
        )
