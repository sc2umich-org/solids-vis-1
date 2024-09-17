import sys
sys.path.append('.')
import sv

sv.render_sv.remove_cube()
sv.render_sv.render("remove_cube","tests", "JPEG")