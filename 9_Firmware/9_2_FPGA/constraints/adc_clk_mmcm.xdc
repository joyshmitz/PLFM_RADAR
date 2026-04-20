# ============================================================================
# adc_clk_mmcm.xdc — Supplementary constraints for MMCM ADC clock path
#
# These constraints augment the existing adc_dco_p clock definitions when the
# adc_clk_mmcm module is integrated into ad9484_interface_400m.v.
#
# USAGE:
#   Add this file to the Vivado project AFTER the main production XDC.
#   The main XDC still defines create_clock on adc_dco_p (the physical input).
#   Vivado automatically creates a generated clock on the MMCM output;
#   these constraints handle CDC paths for the new clock topology.
#
# HIERARCHY: rx_inst/adc/mmcm_inst/...
# ============================================================================

# --------------------------------------------------------------------------
# MMCM Output Clock — use Vivado's auto-generated clock name
# --------------------------------------------------------------------------
# Vivado auto-creates a generated clock named 'clk_mmcm_out0' on the MMCM
# CLKOUT0 net. We do NOT create_generated_clock here (that would create a
# second clock on the same net, causing the CDC false paths below to bind
# to the wrong clock and leave clk_mmcm_out0 uncovered — exactly the bug
# that caused Build 19's -0.011 ns WNS on the CDC_FIR gray-code path).
# All constraints below reference 'clk_mmcm_out0' directly.

# --------------------------------------------------------------------------
# CDC: BUFIO domain (adc_dco_p) ↔ MMCM output domain (clk_mmcm_out0)
# --------------------------------------------------------------------------
# The IDDR outputs are captured by BUFIO (adc_dco_p clock), then re-registered
# into the MMCM BUFG domain in ad9484_interface_400m.v.
# These clocks are frequency-matched and phase-related (MMCM is locked to
# adc_dco_p), so the single register transfer is safe. We use max_delay
# (one period) to ensure the tools verify the transfer fits within one cycle
# without over-constraining with full inter-clock setup/hold analysis.
set_max_delay -datapath_only -from [get_clocks adc_dco_p] \
    -to [get_clocks clk_mmcm_out0] 2.700

set_max_delay -datapath_only -from [get_clocks clk_mmcm_out0] \
    -to [get_clocks adc_dco_p] 2.700

# --------------------------------------------------------------------------
# CDC: MMCM output domain ↔ other clock domains
# --------------------------------------------------------------------------
# The existing false paths in the production XDC reference adc_dco_p, which
# now only covers the BUFIO/IDDR domain. The MMCM output clock (which drives
# all fabric 400 MHz logic) needs its own false path declarations.
set_false_path -from [get_clocks clk_100m] -to [get_clocks clk_mmcm_out0]
set_false_path -from [get_clocks clk_mmcm_out0] -to [get_clocks clk_100m]

# Audit F-0.6: the USB-domain clock name differs per board
# (50T: ft_clkout, 200T: ft601_clk_in). XDC files only support a
# restricted Tcl subset — `foreach`/`unset` trigger CRITICAL WARNING
# [Designutils 20-1307]. The clk_mmcm_out0 ↔ USB-clock false paths
# are declared in the per-board XDC (xc7a50t_ftg256.xdc and
# xc7a200t_fbg484.xdc) where the USB clock name is already known.

set_false_path -from [get_clocks clk_mmcm_out0] -to [get_clocks clk_120m_dac]
set_false_path -from [get_clocks clk_120m_dac] -to [get_clocks clk_mmcm_out0]

# --------------------------------------------------------------------------
# MMCM Locked — asynchronous status signal, no timing paths needed
# --------------------------------------------------------------------------
# LOCKED is not a valid timing startpoint (it's a combinational output of the
# MMCM primitive). Use -through instead of -from to waive all paths that pass
# through the LOCKED net. This avoids the CRITICAL WARNING from Build 19/20.
# Audit F-0.7: the literal hierarchical path was missing the `u_core/`
# prefix and silently matched no pins. Use a hierarchical wildcard to
# catch the MMCM LOCKED pin regardless of wrapper hierarchy.
set_false_path -through [get_pins -hierarchical -filter {REF_PIN_NAME == LOCKED}]

# --------------------------------------------------------------------------
# Hold waiver for source-synchronous ADC capture (BUFIO-clocked IDDR)
# --------------------------------------------------------------------------
# The AD9484 ADC provides a source-synchronous interface: data (adc_d_p/n)
# and clock (adc_dco_p/n) are output from the same chip with matched timing.
# On the PCB, data and DCO traces are length-matched.
#
# Inside the FPGA, the DCO clock path goes through IBUFDS → BUFIO, adding
# ~2.2ns of insertion delay (IBUFDS 0.9ns + routing 0.6ns + BUFIO 1.3ns).
# The data path goes through IBUFDS only (~0.85ns), arriving at the IDDR
# ~1.4ns before the clock. Vivado's hold analysis sees the data "changing"
# before the clock edge and reports WHS = -1.955ns.
#
# This is correct internal behavior: the BUFIO clock intentionally arrives
# after the data. The IDDR captures on the BUFIO edge, by which time the
# data is stable. Hold timing is guaranteed by the external PCB layout
# (ADC data valid window centered on DCO edge), not by FPGA clock tree
# delays. Vivado's STA model cannot account for this external relationship.
#
# Waiving hold on these 8 paths (adc_d_p[0..7] → IDDR) is standard practice
# for source-synchronous LVDS ADC interfaces using BUFIO capture.
set_false_path -hold -from [get_ports {adc_d_p[*]}] -to [get_clocks adc_dco_p]

# --------------------------------------------------------------------------
# Timing margin for 400 MHz critical paths
# --------------------------------------------------------------------------
# Extra setup uncertainty forces Vivado to leave margin for temperature/voltage/
# aging variation. 150 ps absolute covers the built-in jitter-based value
# (~53 ps) plus ~100 ps temperature/voltage/aging guardband.
# NOTE: Vivado's set_clock_uncertainty does NOT accept -add; prior use of
# -add 0.100 was silently rejected as a CRITICAL WARNING, so no guardband
# was applied. Use an absolute value. (audit finding F-0.8)
set_clock_uncertainty -setup 0.150 [get_clocks clk_mmcm_out0]
