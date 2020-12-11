import vapoursynth as vs
from vsutil import plane, depth

core = vs.core

def FaggotDB(src: vs.VideoNode, thrY=40, thrC=None, radiusY=15, radiusC=15, CbY=44, CrY=44, CbC=44, CrC=44, grainY=20, grainC=None, sample_mode=2, neo=False, dynamic_grainY=False, dynamic_grainC=False, tv_range=True, mask=None) -> vs.VideoNode:
    funcName = "FaggotDB"

    if not isinstance(src, vs.VideoNode):
        raise TypeError(f'{funcName}: This is not a clip!')
    
    bits = src.format.bits_per_sample

    if bits < 16:
        src = depth(src, 16)
    if bits > 16:
        src = depth(src, 16)

    if mask is None:
        mask = core.adg.Mask(core.std.PlaneStats(src16), 4).std.Inflate()
        # 'cause I hate GradFun3

    if thrC is None:
        thrC = thrY // 2
    
    if grainC is None:
        graincC = grainY // 2
    
    f3kdb = core.neo_f3kdb.Deband if neo else core.f3kdb.Deband

    U = plane(src, 1)
    V = plane(src, 2)
    
    U = f3kdb(U, range=radiusC, y=thrC, cb=CbC, cr=CrC, grainy=grainC, grainc=0, sample_mode=sample_mode, dynamic_grain=dynamic_grainC, keep_tv_range=tv_range, output_depth=16)
    V = f3kdb(V, range=radiusC, y=thrC, cb=CbC, cr=CrC, grainy=grainC, grainc=0, sample_mode=sample_mode, dynamic_grain=dynamic_grainC, keep_tv_range=tv_range, output_depth=16)

    filtered = core.std.ShufflePlanes([src, U, V], [0, 0, 0], vs.YUV)
    filtered = f3kdb(filtered, range=radiusY, y=thrY, cb=CbY, cr=CrY, grainy=grainY, grainc=0, sample_mode=sample_mode, dynamic_grain=dynamic_grainY, keep_tv_range=tv_range, output_depth=16)

    return depth(core.std.MaskedMerge(filtered, src, mask), bits)
