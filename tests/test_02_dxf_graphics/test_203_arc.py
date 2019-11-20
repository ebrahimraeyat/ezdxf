# Copyright (c) 2019 Manfred Moitzi
# License: MIT License
# created 2019-02-15
import pytest
from ezdxf.math import Vector
from ezdxf.entities.arc import Arc
from ezdxf.lldxf.const import DXF12, DXF2000
from ezdxf.lldxf.tagwriter import TagCollector, basic_tags_from_text

TEST_CLASS = Arc
TEST_TYPE = 'ARC'

ENTITY_R12 = """0
ARC
5
0
8
0
10
0.0
20
0.0
30
0.0
40
1.0
50
0
51
360
"""

ENTITY_R2000 = """0
ARC
5
0
330
0
100
AcDbEntity
8
0
100
AcDbCircle
10
0.0
20
0.0
30
0.0
40
1.0
100
AcDbArc
50
0
51
360
"""


@pytest.fixture(params=[ENTITY_R12, ENTITY_R2000])
def entity(request):
    return TEST_CLASS.from_text(request.param)


def test_registered():
    from ezdxf.entities.factory import ENTITY_CLASSES
    assert TEST_TYPE in ENTITY_CLASSES


def test_default_init():
    entity= TEST_CLASS()
    assert entity.dxftype() == TEST_TYPE
    assert entity.dxf.handle is None
    assert entity.dxf.owner is None


def test_default_new():
    entity = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'color': '7',
        'center': (1, 2, 3),
        'radius': 2.5,
        'start_angle': 30,
        'end_angle': 290,
    })
    assert entity.dxf.layer == '0'
    assert entity.dxf.color == 7
    assert entity.dxf.linetype == 'BYLAYER'

    assert entity.dxf.center == (1, 2, 3)
    assert entity.dxf.center.x == 1, 'is not Vector compatible'
    assert entity.dxf.center.y == 2, 'is not Vector compatible'
    assert entity.dxf.center.z == 3, 'is not Vector compatible'
    assert entity.dxf.radius == 2.5
    assert entity.dxf.start_angle == 30
    assert entity.dxf.end_angle == 290
    # can set DXF R2007 value
    entity.dxf.shadow_mode = 1
    assert entity.dxf.shadow_mode == 1
    assert entity.dxf.extrusion == (0.0, 0.0, 1.0)
    assert entity.dxf.hasattr('extrusion') is False, 'just the default value'


def test_get_start_and_end_point_with_ocs():
    radius = 2.5
    z = 3.0
    arc = TEST_CLASS.new(handle='ABBA', owner='0', dxfattribs={
        'center': (1, 2, z),
        'radius': radius,
        'start_angle': 90,
        'end_angle': 180,
        'extrusion': (0, 0, -1),
    })

    assert arc.start_point.isclose(Vector(0, radius, -z), abs_tol=1e-6)
    assert arc.end_point.isclose(Vector(radius, 0, -z), abs_tol=1e-6)


def test_load_from_text(entity):
    assert entity.dxf.layer == '0'
    assert entity.dxf.color == 256, 'default color is 256 (by layer)'
    assert entity.dxf.center == (0, 0, 0)
    assert entity.dxf.radius == 1
    assert entity.dxf.start_angle == 0
    assert entity.dxf.end_angle == 360


@pytest.mark.parametrize("txt,ver", [(ENTITY_R2000, DXF2000), (ENTITY_R12, DXF12)])
def test_write_dxf(txt, ver):
    expected = basic_tags_from_text(txt)
    arc = TEST_CLASS.from_text(txt)
    collector = TagCollector(dxfversion=ver, optional=True)
    arc.export_dxf(collector)
    assert collector.tags == expected

    collector2 = TagCollector(dxfversion=ver, optional=False)
    arc.export_dxf(collector2)
    assert collector.has_all_tags(collector2)
