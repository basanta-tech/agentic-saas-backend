from fastapi import HTTPException

class TodoError(HTTPException):
  """Base exception for todo-related errors"""
  pass

class TodoNotFoundError(TodoError):
  def __init__(self, todo_id=None):
    message = "Todo not found" if todo_id is None else f"Todo with id {todo_id} not found"
    super().__init__(status_code=404, detail=message)

class TodoCreationError(TodoError):
  def __init__(self, error: str):
    super().__init__(status_code=500, detail=f"Failed to create todo: {error}")




class AgentError(HTTPException):
  """Base exception for agent-related errors"""
  pass

class AgentNotFoundError(AgentError):
  def __init__(self, agent_id=None):
    message = "Todo not found" if agent_id is None else f"Todo with id {agent_id} not found"
    super().__init__(status_code=404, detail=message)

class AgentCreationError(AgentError):
  def __init__(self, error: str):
    super().__init__(status_code=500, detail=f"Failed to create agent: {error}")



class TenantError(HTTPException):
  """Base exception for tenant-related errors"""
  pass

class TenantNotFoundError(TenantError):
  def __init__(self, tenant_id=None):
    message = "Tenant not found" if tenant_id is None else f"Tenant with id {tenant_id} not found"
    super().__init__(status_code=404, detail=message)

class TenantCreationError(TenantError):
  def __init__(self, error: str):
    super().__init__(status_code=500, detail=f"Failed to create agent: {error}")



class UserError(HTTPException):
  """Base exception for user-related errors"""
  pass

class UserNotFoundError(UserError):
  def __init__(self, user_id=None):
    message = "User not found" if user_id is None else f"User with id {user_id} not found"
    super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
  def __init__(self):
    super().__init__(status_code=400, detail="New passwords do not match")

class InvalidPasswordError(UserError):
  def __init__(self):
    super().__init__(status_code=401, detail="Current password is incorrect")

class AuthenticationError(HTTPException):
  def __init__(self, message: str = "Could not validate user"):
    super().__init__(status_code=401, detail=message)
