#from vapoursynth import core, VideoNode, GRAY, YUV
import vapoursynth as vs
import fvsfunc as fvf # https://github.com/Irrational-Encoding-Wizardry/fvsfunc/blob/master/fvsfunc.py
from vsutil import plane # https://github.com/Irrational-Encoding-Wizardry/vsutil/blob/master/vsutil.py

core = vs.core

def FaggotDB(clip: vs.VideoNode, thrY=40, thrC=None, radiusY=15, radiusC=15, CbY=44, CrY=44, CbC=44, CrC=44, grainY=20, grainC=None, sample_mode=2, neo=False, dynamic_grainY=False, dynamic_grainC=False, tv_range=True, mask=None) -> vs.VideoNode:

    funcName = "FaggotDB"

    # Original Idea: Author who created Fag3kdb. Edited by AlucardSama04

    if not isinstance(clip, vs.VideoNode):
        raise TypeError(f"{funcName}: This is not a clip")

    if clip.format.bits_per_sample != 16:
        raise TypeError(f"{funcName}: Only 16Bit clips are supported")

    if not isinstance(mask, vs.VideoNode):
        raise vs.Error(f"{funcName}: mask' only clip inputs")

    if thrC is None:
        thrC = int(round(thrY / 2))

    if grainC is None:
        grainC = int(round(grainY / 2))

    f3kdb = core.neo_f3kdb.Deband if neo else core.f3kdb.Deband

    U = plane(clip, 1)
    V = plane(clip, 2)
    U = f3kdb(U, range=radiusC, y=thrC, cb=CbC, cr=CrC, grainy=grainC, grainc=0, sample_mode=sample_mode, dynamic_grain=dynamic_grainC, keep_tv_range=tv_range, output_depth=16)

    V = f3kdb(V, range=radiusC, y=thrC, cb=CbC, cr=CrC, grainy=grainC, grainc=0, sample_mode=sample_mode, dynamic_grain=dynamic_grainC, keep_tv_range=tv_range, output_depth=16)

    filtered = core.std.ShufflePlanes([clip,U,V], [0,0,0], vs.YUV)
    filtered = f3kdb(filtered, range=radiusY, y=thrY, cb=CbY, cr=CrY, grainy=grainY, grainc=0, sample_mode=sample_mode, dynamic_grain=dynamic_grainY, keep_tv_range=tv_range, output_depth=16)

    return core.std.MaskedMerge(filtered, clip, mask)
