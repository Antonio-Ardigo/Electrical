# Master Single-Line Diagram — 2 MW MV/LV Process Plant

> Complete reference SLD for the ~2 MW process plant. This is the canonical
> single-line referenced by Module 1. Tags follow the design basis in
> `docs/main-electrical-equipment-2MW-process-plant.md`.
> Concept-level; ratings indicative and to be confirmed by detailed studies.

```
                              UTILITY MV FEED
                              11 kV, 3-phase, 50 Hz
                                     │
                                     │
                            ┌────────┴────────┐
                            │     MV-MET      │   Revenue metering cubicle
                            │   CT / VT, kWh  │   (tariff meter, utility CTs/VTs)
                            └────────┬────────┘
                                     │
        ╔════════════════════════════╪════════════════════════════╗
        ║  MV-SWGR — 11 kV METAL-CLAD SWITCHGEAR (IEC 62271-200)   ║
        ║                            │                             ║
        ║                          [52-I]   Incomer CB (vacuum)    ║
        ║                            │       MV-PROT 50/51,50N/51N  ║
        ║   MV-NER ───────[N]════════╪════════════════════[BUS 11kV]║
        ║   Neutral Earthing         │            ║                ║
        ║   Resistor (limits IEF     │          [52-BS]  Bus-      ║
        ║   ~300-400 A) + neutral CT │            ║      section CB ║
        ║                    ┌───────┴──────┐  ┌──╨───────────┐    ║
        ║                  [52-T1]        [52-T2]              │    ║
        ║                Tx-1 feeder    Tx-2 feeder                ║
        ║                  87T diff.      87T diff.                ║
        ╚════════════════════╪══════════════════╪═════════════════╝
                             │                  │
                       ┌─────┴─────┐      ┌─────┴─────┐
                       │   TX-1    │      │   TX-2    │
                       │ 1600 kVA  │      │ 1600 kVA  │   Dyn11, Z≈6%
                    8 (│11kV/0.4kV│)8  8 (│11kV/0.4kV│)8  IEC 60076
                       │  Dyn11    │      │  Dyn11    │
                       └─────┬─────┘      └─────┬─────┘
                             │                  │
                          [ACB-A]            [ACB-B]   LV incomer ACBs
                             │                  │
   ╔═════════════════════════╪══════════════════╪═════════════════════════╗
   ║  LV-MSB — MAIN LV SWITCHBOARD / PCC   400 V, 50-65 kA, IEC 61439     ║
   ║                         │                  │                         ║
   ║   ════ BUS A ═══════════╪════   N.O.   ════╪═══════════ BUS B ════   ║
   ║          │      │       │   [BT]══════════  │       │      │         ║
   ║          │      │       │  bus-tie (N.O.,   │       │      │         ║
   ║          │      │       │  auto-close on    │       │      │         ║
   ║          │      │       │  loss of incomer) │       │      │         ║
   ╚══════════╪══════╪═══════╪═══════════════════╪═══════╪══════╪═════════╝
              │      │       │                   │       │      │
            [MCCB] [MCCB]  [MCCB]              [MCCB]  [MCCB] [MCCB]
              │      │       │                   │       │      │
          ┌───┴──┐ ┌─┴──┐ ┌──┴───┐          ┌────┴──┐ ┌──┴─┐ ┌─┴────┐
          │ MCC-1│ │PFC │ │ DB-A │          │ MCC-2 │ │UPS │ │ EDB  │
          │      │ │cap │ │light │          │       │ │    │ │essntl│
          └───┬──┘ │bank│ │/power│          └───┬───┘ └─┬──┘ └──┬───┘
              │    │det.│ └──────┘              │       │       │
              │    │7%  │                       │       │       ▲
        ┌─────┼────┴────┐                 ┌─────┼─────┐ │       │ fed via ATS
        │     │         │                 │     │     │ │       │
      [DOL] [VFD]    [S/S]              [VFD] [DOL] [S/S]│       │
        │     │         │                 │     │     │ │       │
        M     M         M                 M     M     M │       │
      pump  proc.    convey.           pump  fan   mixer│       │
            motor                                       │       │
                                          ┌─────────────┴────┐  │
                                          │       UPS        │  │
                                          │  + static bypass │  │
                                          └────────┬─────────┘  │
                                                   │            │
                                          DCS / PLC / SCADA     │
                                          Instrumentation       │
                                                                │
   ─────────────────────────────────────────────────────────── │ ──────────
   STANDBY POWER PATH                                           │
                                                                │
        ┌──────────┐                          ┌────────┐       │
        │   DG     │                          │  ATS   │       │
        │ diesel   │──────────────────────────│ Util ↔ │───────┘
        │ gen set  │   essential-load feed    │  DG    │   to EDB / Essential bus
        │ 1000 kVA │                          └────────┘
        └──────────┘
   ─────────────────────────────────────────────────────────────────────────
   DC CONTROL / PROTECTION SUPPLY
                                          ┌──────────────────┐
        MV-SWGR trip/close & protection ──│      DCDB        │
        relays (110 V DC)                 │ battery+charger  │
                                          │  110 V DC        │
                                          └──────────────────┘
```

## Notes on conventions

- `[52-x]` = MV circuit breaker (ANSI 52); `[ACB]`/`[MCCB]` = LV breakers.
- `═══` busbars; `(│ │)` with `8` = transformer windings (Dyn11).
- `N.O.` = normally-open bus-tie (auto-closes on loss of one incomer).
- `M` = motor; DOL / S/S (soft-starter) / VFD denote the starter type.
- `[N]` on MV-NER = neutral point connection through the earthing resistor.

## Tag Legend

| Tag | Description |
|-----|-------------|
| <a id="mv-met"></a>MV-MET | Utility revenue metering cubicle (CTs/VTs, tariff kWh meter) at the 11 kV incomer. |
| <a id="mv-swgr"></a>MV-SWGR | 11 kV metal-clad switchgear: incomer CB, bus-section CB, two transformer feeders; vacuum CBs, 25 kA/1 s, IEC 62271-200. |
| <a id="mv-prot"></a>MV-PROT | MV protection & control IEDs: 50/51, 50N/51N overcurrent/earth-fault, 87T transformer differential, 27/59. |
| <a id="mv-ner"></a>MV-NER | Neutral Earthing Resistor — limits MV earth-fault current (~300–400 A) with neutral CT. |
| <a id="tx-1"></a>TX-1 | MV/LV power transformer No.1 — 1600 kVA, 11 kV/0.4 kV, Dyn11, Z≈6%, IEC 60076. Feeds LV-MSB Bus A. |
| <a id="tx-2"></a>TX-2 | MV/LV power transformer No.2 — 1600 kVA, 11 kV/0.4 kV, Dyn11, Z≈6%, IEC 60076. Feeds LV-MSB Bus B. |
| <a id="lv-msb"></a>LV-MSB | Main LV switchboard / Power Control Centre — 400 V, split bus A/B, 2500–3200 A, 50–65 kA, ACB incomers + motorized N.O. bus-tie, IEC 61439-1/2. |
| <a id="bt"></a>BT | LV bus-tie circuit breaker — normally-open; auto-closes on loss of either incomer to maintain supply to the surviving bus. |
| <a id="mcc-1"></a>MCC-1 | Motor Control Centre No.1 (on Bus A) — DOL / star-delta / soft-starter / VFD buckets, IEC 61439-1/2. |
| <a id="mcc-2"></a>MCC-2 | Motor Control Centre No.2 (on Bus B) — DOL / soft-starter / VFD buckets, IEC 61439-1/2. |
| <a id="vfd"></a>VFD | Variable Frequency Drive(s) for speed-controlled pumps/fans/mixers; input chokes/EMC filters, IEC 61800. |
| <a id="pfc"></a>PFC | Power factor correction — automatic, detuned (7%) capacitor bank; corrects ~0.85 → 0.95+, IEC 60831. |
| <a id="db"></a>DB / DB-A | Distribution board — lighting, small power, HVAC, sockets; MCB/RCBO. |
| <a id="edb"></a>EDB | Essential / emergency distribution board — fed via ATS from DG. |
| <a id="dg"></a>DG | Diesel generator set — sized for essential loads (~1000 kVA); AVR, day-tank, acoustic canopy. |
| <a id="ats"></a>ATS | Automatic Transfer Switch — Utility ↔ DG changeover for the essential bus. |
| <a id="ups"></a>UPS | Uninterruptible Power Supply for DCS/PLC/SCADA & instrumentation; static bypass, battery autonomy 15–30 min. |
| <a id="dcdb"></a>DCDB | DC battery & charger system — 110 V DC supply for MV switchgear trip/close & protection. |

---

*Concept-level reference SLD. Final ratings, redundancy, earthing and voltage
levels to be confirmed against the load list, short-circuit/load-flow studies,
utility connection agreement and governing standards.*
