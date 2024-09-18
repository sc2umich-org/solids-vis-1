
import sys
sys.path.append('.')
import sv



if __name__=="__main__":
    obj = sv.AnimatedObject.AnimatedObject([0,0,0],"uv_sphere")
    sv.render_sv.remove_cube()
    sv.render_sv.render("added sphere","tests", "JPEG")