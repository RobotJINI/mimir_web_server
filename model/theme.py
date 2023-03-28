
class DefaultTheme():
    def __init__(self):
        self._color1 = '#FA9F42'
        self._color2 = '#2B4162'
        self._color3 = '#0B6E4F'
        self._color4 = '#E0E0E2'
        self._color5 = '#721817'
        
    def get_air(self):
        return self._color2
    
    def get_ground(self):
        return self._color1 
    
    def get_background_fill(self):
        return self._color4