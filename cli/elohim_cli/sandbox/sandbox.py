from RestrictedPython import compile_restricted, safe_globals

class DragonDreamSandbox:
    def __init__(self):
        self.allowed_globals = safe_globals.copy()
        # Add basic math/game logic if needed here
        
    def execute(self, code: str, context: dict):
        try:
            byte_code = compile_restricted(code, '<spell>', 'exec')
            exec(byte_code, self.allowed_globals, context)
            return True, None
        except Exception as e:
            return False, str(e)
