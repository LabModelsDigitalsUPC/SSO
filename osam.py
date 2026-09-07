"""Pydantic v2 schema for the OSAM (Open Structural Analysis Model) format.

Field names match the reference JSON format, but section/load bodies are
flattened directly onto their parent model (no nested `section`/`load`
wrapper key) and `BeamSection.cross_section` is a required, typed
`CrossSectionProfile` rather than an open dict.
"""

from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

# Accepts null JSON values for string fields by coercing None → "".
# Still rejects actual type mismatches (e.g. dict/list where str expected).
NullableStr = Annotated[str, BeforeValidator(lambda v: "" if v is None else v)]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


# ── Primitives ────────────────────────────────────────────────────────────────

class Units(StrictModel):
    force: str = "KILONEWTON"
    length: str = "METRE"
    temperature: str = "CELSIUS"
    time: str = "SECOND"
    mass: str = "KILOGRAM"


class Vector3D(StrictModel):
    X: float
    Y: float
    Z: float


class CoordinateSystem(StrictModel):
    xAxis: Vector3D
    yAxis: Vector3D
    zAxis: Vector3D


# ── Mesh ─────────────────────────────────────────────────────────────────────

class Node(StrictModel):
    X: float
    Y: float
    Z: float
    id: int


class Element(StrictModel):
    id: int
    type: NullableStr = ""
    dofs: list[int] = []
    node_count: int = 0
    face_count: int = 0
    integration: NullableStr = "REDUCED"
    nodes: list[int] = []
    faces: Optional[list[list[int]]] = None
    section: NullableStr = ""
    material: NullableStr = ""


class Mesh(StrictModel):
    node_count: int
    el_count: int
    nodes: list[Node]
    elements: list[Element]


# ── Object ─────────────────────────────────────────────────────────

class Object(StrictModel):
    id: str
    name: str
    mesh: Mesh
    coordinateSystem: CoordinateSystem


# ── Assembly ──────────────────────────────────────────────────────────────────

class Nsets(StrictModel):
    name: str
    nodeIDs: list[int]


class Elsets(StrictModel):
    name: str
    elementIDs: list[int]


class Instance(StrictModel):
    id: str
    name: str
    referenced_object: str
    nsets: list[Nsets] = []
    elsets: list[Elsets] = []
    translation: Optional[Any] = None
    rotation: Optional[Any] = None


class Assembly(StrictModel):
    name: str = "assembly-default"
    instances: list[Instance]


# ── Materials ─────────────────────────────────────────────────────────────────

class ElasticParam(StrictModel):
    E: float = 0.0
    v: float = 0.0


class Elastic(StrictModel):
    behaviour_type: str = "ISOTROPIC"
    parameters: Optional[ElasticParam] = None


class Plastic(StrictModel):
    model_config = ConfigDict(extra="allow")
    yield_stress: Optional[float] = None
    plastic_strain: Optional[float] = None
    functions: Optional[Any] = None


class Material(StrictModel):
    name: str
    category: Optional[str] = None
    type: NullableStr = "ISOTROPIC"
    mass_density: float = 0.0
    elastic: Elastic = Field(default_factory=Elastic)
    plastic: Optional[Plastic] = None


# ── Sections ──────────────────────────────────────────────────────────────────
#
# thickness is the SHELL SECTION's single geometric parameter (metres).

# ── Parametric beam cross-sections ──────────────────────────────────────────
#
# Typed definitions for the beam profile kinds handled by the IFC and INP
# converters (app/converters/ifc/*.py, app/converters/inp/*.py). This union is
# `BeamSection.cross_section`'s type, discriminated on `type`.
# All lengths are metres, matching the rest of the OSAM format.

BeamProfileType = Literal[
    "RECT", "BOX", "PIPE", "CIRC", "I", "L", "HEX", "TRAPEZOID",
    "GENERAL", "NON LINEAR GENERAL", "ARBITRARY",
]


class RectProfile(StrictModel):
    """Solid rectangle: width `a`, height `b`."""
    type: Literal["RECT"]
    a: float = 0.0
    b: float = 0.0


class BoxProfile(StrictModel):
    """Rectangular hollow section: outer width/height `a`/`b`, wall
    thicknesses `t1`-`t4` (the IFC converter requires all four equal)."""
    type: Literal["BOX"]
    a: float = 0.0
    b: float = 0.0
    t1: float = 0.0
    t2: float = 0.0
    t3: float = 0.0
    t4: float = 0.0


class PipeProfile(StrictModel):
    """Circular hollow section: outer radius `r`, wall thickness `t`."""
    type: Literal["PIPE"]
    r: float = 0.0
    t: float = 0.0


class CircProfile(StrictModel):
    """Solid circular section.

    Note: the IFC converter reads/writes this shape's radius under the key
    `radius`, while the INP converter uses `r` for the same shape — a
    pre-existing inconsistency between the two converters, documented here
    but not changed.
    """
    type: Literal["CIRC"]
    radius: float = 0.0


class IProfile(StrictModel):
    """I-shape: overall depth `h`, flange widths `b1`/`b2`, flange
    thicknesses `t1`/`t2`, web thickness `t3`. `l` is the optional Abaqus
    flange-offset parameter present only in the 7-value INP form."""
    type: Literal["I"]
    h: float = 0.0
    b1: float = 0.0
    b2: float = 0.0
    t1: float = 0.0
    t2: float = 0.0
    t3: float = 0.0
    l: Optional[float] = None


class LProfile(StrictModel):
    """L-shape (angle): leg widths `a`/`b`, leg thicknesses `t1`/`t2` (the
    IFC converter requires `t1 == t2`)."""
    type: Literal["L"]
    a: float = 0.0
    b: float = 0.0
    t1: float = 0.0
    t2: float = 0.0


class HexProfile(StrictModel):
    """Hexagonal hollow section (INP-only): circumscribed radius `circ_r`,
    wall thickness `t`."""
    type: Literal["HEX"]
    circ_r: float = 0.0
    t: float = 0.0


class TrapezoidProfile(StrictModel):
    """Trapezoid (INP-only): bottom/top widths `a`/`b`, height `c`, and
    top-edge horizontal offset `d`."""
    type: Literal["TRAPEZOID"]
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0
    d: float = 0.0


class GeneralProfile(StrictModel):
    """Direct section properties, no shape: area `A`, moments of inertia
    `I11`/`I12`/`I22`, torsional constant `J`."""
    type: Literal["GENERAL", "NON LINEAR GENERAL"]
    A: float = 0.0
    I11: float = 0.0
    I12: float = 0.0
    I22: float = 0.0
    J: float = 0.0


class ArbitraryProfile(StrictModel):
    """Arbitrary polygon, optionally with holes."""
    type: Literal["ARBITRARY"]
    edge_points: list[list[float]] = []
    void_points: list[list[list[float]]] = []


CrossSectionProfile = Annotated[
    Union[
        RectProfile, BoxProfile, PipeProfile, CircProfile, IProfile,
        LProfile, HexProfile, TrapezoidProfile, GeneralProfile,
        ArbitraryProfile,
    ],
    Field(discriminator="type"),
]


class BeamSection(StrictModel):
    id: str
    name: str
    section_type: Literal["BEAM SECTION"]
    beam_section: str
    orientation: list[float] = [0, 0, -1]
    cross_section: CrossSectionProfile
    material: Optional[str] = None


class ShellSection(StrictModel):
    id: str
    name: str
    section_type: Literal["SHELL SECTION"]
    thickness: float
    material: Optional[str] = None


class SolidSection(StrictModel):
    id: str
    name: str
    section_type: Literal["SOLID SECTION"]
    material: Optional[str] = None


Section = Annotated[
    Union[BeamSection, ShellSection, SolidSection],
    Field(discriminator="section_type"),
]


# ── Boundary conditions ───────────────────────────────────────────────────────

class BoundaryCondition(StrictModel):
    id: str
    type: NullableStr = "DISPLACEMENT"
    nset: str
    instances: Optional[list[str]] = None
    ux: list[Union[bool, float]] = []
    uy: list[Union[bool, float]] = []
    uz: list[Union[bool, float]] = []
    rx: list[Union[bool, float]] = []
    ry: list[Union[bool, float]] = []
    rz: list[Union[bool, float]] = []


# ── Load cases ────────────────────────────────────────────────────────────────

class LoadCase(StrictModel):
    id: str
    name: str
    type: NullableStr = ""
    selfWeight: list[float] = [0.0, 0.0, 0.0]


# ── Loads ─────────────────────────────────────────────────────────────────────

class PointLoad(StrictModel):
    id: str
    type: Literal["POINT_LOAD"]
    caseName: str
    instances: Optional[list[str]] = None
    nset: str
    dof: int
    v: float


class DistributedLoad(StrictModel):
    id: str
    type: Literal["DISTRIBUTED_LOAD"]
    caseName: str
    instances: Optional[list[str]] = None
    elset: str
    dir: str
    v1: float
    v2: float
    x1: float
    x2: float


class SurfaceLoad(StrictModel):
    id: str
    type: Literal["SURFACE_LOAD"]
    caseName: str
    instances: Optional[list[str]] = None
    elset: str
    v: float
    xdir: float
    ydir: float
    zdir: float


Load = Annotated[
    Union[PointLoad, DistributedLoad, SurfaceLoad],
    Field(discriminator="type"),
]



# ── Root model ────────────────────────────────────────────────────────────────

class StructuralAnalysisModel(StrictModel):
    id: str
    name: str
    units: Units = Field(default_factory=Units)
    objects: list[Object]
    assembly: Assembly
    materials: list[Material] = []
    sections: list[Section] = []
    bc: list[BoundaryCondition] = []
    loadCases: list[LoadCase] = []
    loads: list[Load] = []
