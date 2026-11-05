# Konvention über die Divergenz: bei rundlichen Details haben dR/dSpalte und dG/dZeile
# bei OpenGL entgegengesetzte Vorzeichen (Korrelation < 0), bei DirectX gleiche (> 0)
import sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
n = np.asarray(Image.open(sys.argv[1]).convert('RGB'), float) / 255
r = gaussian_filter(n[..., 0], 1.0); g = gaussian_filter(n[..., 1], 1.0)
a = np.gradient(r, axis=1); b = np.gradient(g, axis=0)
m = (np.abs(a) + np.abs(b)) > np.percentile(np.abs(a) + np.abs(b), 80)
c = np.corrcoef(a[m], b[m])[0, 1]
print('%-36s Korr = %+.3f  -> %s' % (sys.argv[1].split('/')[-1], c, 'OpenGL' if c < 0 else 'DirectX'))
