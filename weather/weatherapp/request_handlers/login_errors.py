class LoginError(Exception):
    def __init__(self, descripition: str) -> None:
        self.description: str = descripition
        
    def __str__(self) -> str:
        return self.description
    
    def tmp(self) -> None:
        if request.POST and is_login_data_correct(request.POST):
            user_name = request.POST['user_login']
            request.session['username'] = username   
        elif 'username' in request.session:
            username = request.session['username']
            