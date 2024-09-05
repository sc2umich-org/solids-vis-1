
import sys
sys.path.append('.')

import sv



# if __name__=="__main__":
obj = sv.AnimatedObject.AnimatedObject([0,0,0],"cube")
sv.render_sv.render("added object", "JPEG")