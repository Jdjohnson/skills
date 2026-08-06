# Circuit Schematic

## Defining grammar

Circuit Schematic represents electrical function through standardized symbols and connected nets rather than physical appearance. Resistors, capacitors, sources, switches, logic elements, grounds, connectors, and other components are abstracted so the reader can trace relationships. Reference designators, net names, values, junctions, functional blocks, and input-to-output flow make the system inspectable. The direction requires a complete plausible topology; decorative circuit traces and photographs of printed boards are different visual forms.

## Composition and type

Arrange signal or power flow consistently, often left to right or top to bottom, while keeping supply rails and ground conventions clear. Group related components into functional stages and label blocks when the whole system is complex. Minimize wire crossings, distinguish connected junctions from passing lines, and use buses or named nets when long connections would obscure structure. Component IDs and values should sit close to symbols without colliding. Typography must be compact, monospaced or technical, and readable at working scale. Avoid arbitrary symbols, dangling nets, and labels that do not correspond to the circuit.

## Color, material, imagery, and light

Traditional schematics use black line on white or cream, blue diazo reproduction, or crisp digital line with one or two semantic colors. Line weight should be uniform enough to trace but varied subtly for blocks, buses, or emphasis. No modeled light is needed. Paper folds, pencil corrections, or scan character may belong to a historical drawing, but modern work should remain clean. Color may separate power, signal, ground, or subsystem only when a legend makes the meaning explicit.

## Common exits

The style exits into Engineering Blueprint when physical dimensions, orthographic views, materials, and title-block construction information dominate. It exits into Operational Dashboard when live system status and controls replace electrical topology. It exits into PCB layout when copper traces, pads, layers, footprints, and board geometry show physical realization. A tech background made of glowing lines, microchip photograph, or disconnected symbol pattern is not a circuit schematic.

## Medium adaptation

For editorial explanation, simplify to the minimum circuit that still demonstrates the function and label any omitted detail. For presentation, reveal functional blocks first and then open one block into components. For interfaces, allow pan, zoom, net highlighting, and cross-reference without changing symbol meaning. Motion can trace current or signal state carefully, but should not imply direction where alternating or bidirectional behavior differs. Validate real circuits with engineering tools or a qualified reviewer; when the schematic is illustrative, keep values and connections internally coherent and avoid suggesting production readiness.
