import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

col1, col2 = st.columns(2)

obs_data = col1.checkbox('Observational data?')
if obs_data:
    px = col1.slider('$P(x)$', 0.0, 1.0, .5, step=0.01)
    pyx = col2.slider('$P(y|x)$', 0.0, 1.0, .5, step=0.01)
    pyxp = col2.slider("$P(y|x')$", 0.0, 1.0, .5, step=0.01)
    pxy = pyx*px
    pxyp = (1-pyx)*px
    pxpy = pyxp*(1-px)
    pxpyp = (1-pyxp)*(1-px)
    first_upper_bound = pxy + pxpyp

fig, ax = plt.subplots()

def lower(ate):
    return max(0, ate)
def upper(ate):
    return min(first_upper_bound, max(0, ate + pxpy + pxyp))

if obs_data:
    ates = np.linspace(-1, 1, num=201)
    lowers = list(map(lower, ates))
    uppers = np.array(list(map(upper, ates)))
    plt.stackplot(ates,
                  lowers,
                  np.clip(uppers - lowers, 0, None),
                  alpha = 0.5,
                  colors =['w', 'g'])
    left_incompatible_ate = first_upper_bound - 1
    right_incompatible_ate = first_upper_bound
    ax.add_patch(patches.Rectangle((-1, 0),
                                   left_incompatible_ate + 1,
                                   1,
                                   facecolor='black',
                                   alpha=0.4,
                                   fill=True))
    ax.add_patch(patches.Rectangle((right_incompatible_ate, 0),
                                   1 - right_incompatible_ate,
                                   1,
                                   facecolor='black',
                                   alpha=0.4,
                                   fill=True))
else:
    plt.stackplot([-1, 0, 1], [0,0,1], [0,1,0], alpha = 0.5, colors =['w', 'g'])

plt.xlabel('ATE')
plt.ylabel('PNS')
plt.title('Lower and Upper PNS bounds vs ATE')
st.pyplot(fig)

if obs_data:
    st.write(f"$P(x, y)={pxy:.3f}, P(x, y')={pxyp:.3f}, P(x', y)={pxpy:.3f}, P(x', y')={pxpyp:.3f}$")
